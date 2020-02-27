import email
import googletrans
import imaplib
from imapclient import imap_utf7
import io
from email import policy
import re
import socket


class MyIMAP:
    def __init__(self, address, password):
        self.address = address
        self.password = password
        self.errors = []

    def get_connect(self):
        try:
            server_name = 'imap.' + self.address[self.address.find('@')+1:]
            imap = imaplib.IMAP4_SSL(server_name)
            imap.login(self.address, self.password)
            return imap
        except imaplib.IMAP4.error:
            self.errors = ('Авторизация невозможна! Логин или пароль некорректны!',)
        except socket.gaierror:
            self.errors = ('Не удалось подключиться к серверу, попробуйте попозже!',)
        except UnicodeEncodeError:
            self.errors = ('Пароль и адрес почты должен содержать только цифры и буквы латинского алфавита!',)

    def messages_list(self, page, per_page, mailbox):
        total, messages_list, mailbox_list = 0, [], dict()
        imap = self.get_connect()
        try:
            if imap:
                mailbox_list = self.mailboxes_list(imap)
                resp, total = imap.select(mailbox_list.get(mailbox)[1], readonly=True)
                if resp == 'NO':
                    self.errors, total = ('Выбранный ящик отсутствует!',), 0
                else:
                    total = int(str(total[0], 'utf-8'))
                    code, data = imap.uid('search', None, 'All')
                    if data[0]:
                        msgs_uids = data[0].decode('utf-8').split()
                        msgs_uids = self.slice_uid_list(page, per_page, total, msgs_uids)
                        code, data = imap.uid('fetch', ','.join(msgs_uids), '(RFC822)')
                        data = [data[i] for i in range(0, len(data), 2)]    # remove b')' item
                        code, unseen = imap.uid('search', None, '(UNSEEN)')
                        unseen = unseen[0].decode('utf-8')
                        messages_list = self.parse_messages_info(data, msgs_uids, unseen)
        except TypeError:
            self.errors = ('Запрашиваемый почтовый ящик не найден!',)
        except imaplib.IMAP4_SSL.error:
            self.errors = ('Нужная страница не найдена!',)
        return total, messages_list, mailbox_list

    def mailboxes_list(self, imap):
        mailboxes = dict()
        translator = googletrans.Translator()
        for box in imap.list()[1]:
            box = box.split(b' "/" ')[1]
            mailbox = imap_utf7.decode(box)[1:-1]
            box = box.decode('utf-8')
            if mailbox == '[Gmail]':
                continue
            elif mailbox == 'INBOX':
                mailboxes['inbox'] = ('Входящие', box)
            else:
                mailbox = mailbox.replace('[Gmail]/', '')
                ind = translator.translate(mailbox, 'en').text.lower().replace(' ', '').replace('/', '-')
                mailboxes[ind] = (mailbox, box)
        return mailboxes

    def read_msg(self, mailbox, uid):
        mailboxes_list, message = [], {}
        imap = self.get_connect()
        try:
            if imap:
                mailboxes_list = self.mailboxes_list(imap)
                resp, total = imap.select(mailboxes_list[mailbox][1])
                if resp == 'OK':
                    resp, data = imap.uid('fetch', str(uid), '(RFC822)')
                    msg = email.message_from_bytes(data[0][1], policy=policy.default)
                    content = self.get_body(msg).decode('utf-8')
                    content = re.sub('\r\n', '<br>', content) if content.find('<head>') < 0 else content
                    message = {'uid': uid, 'From': msg['From'], 'To': msg['To'], 'Subject': msg['Subject'],
                               'Content': content, 'Attachments': []}
                    for part in msg.walk():
                        if part.get_filename():
                            message['Attachments'].append(part.get_filename())
        except TypeError:
            self.errors = ('Запрашиваемый почтовый ящик не найден!',)
        return message

    def download(self, mailbox, filename, uid):
        file = io.BytesIO()
        imap = self.get_connect()
        try:
            if imap:
                mailboxes_list = self.mailboxes_list(imap)
                resp, total = imap.select(mailboxes_list[mailbox][1])
                if resp == 'OK':
                    resp, data = imap.uid('fetch', str(uid), '(RFC822)')
                    msg = email.message_from_bytes(data[0][1], policy=policy.default)
                    for part in msg.walk():
                        if part.get_filename() == filename:
                            file.write(part.get_payload(decode=True))
                            file.seek(0)
                            break
        except TypeError:
            self.errors = ('Запрашиваемый почтовый ящик не найден!',)
        return file

    def get_body(self, msg):
        if msg.is_multipart():
            return self.get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)

    def mark_seen(self, uid_list, mailbox):
        imap = self.get_connect()
        try:
            if imap:
                mailboxes_list = self.mailboxes_list(imap)
                resp, total = imap.select(mailboxes_list[mailbox][1])
                if resp == 'OK':
                    resp, data = imap.uid('store', ','.join(uid_list), '+FLAGS', '\\SEEN')
                    if resp == 'OK':
                        return True
        except TypeError:
            self.errors = ('Запрашиваемый почтовый ящик не найден!',)

    def mark_unseen(self, uid_list, mailbox):
        imap = self.get_connect()
        try:
            if imap:
                mailboxes_list = self.mailboxes_list(imap)
                resp, total = imap.select(mailboxes_list[mailbox][1])
                if resp == 'OK':
                    resp, data = imap.uid('store', ','.join(uid_list), '-FLAGS', '\\SEEN')
                    if resp == 'OK':
                        return True
        except TypeError:
            self.errors = ('Запрашиваемый почтовый ящик не найден!',)

    def mark_deleted(self, uid_list, mailbox):
        imap = self.get_connect()
        try:
            if imap:
                mailboxes_list = self.mailboxes_list(imap)
                resp, total = imap.select(mailboxes_list[mailbox][1])
                if resp == 'OK':
                    resp, data = imap.uid('store', ','.join(uid_list), '+FLAGS', '\\DELETED')
                    if resp == 'OK':
                        imap.expunge()
                        return True
        except TypeError:
            self.errors = ('Запрашиваемый почтовый ящик не найден!',)

    def slice_uid_list(self, page, per_page, total, uid_list):
        end = page * per_page
        start = end - per_page
        end = end - (end - total - 1) if end > total else end
        result = uid_list[-end:-start] if start != 0 else uid_list[-end:]
        return result

    def parse_messages_info(self, data, uid_list, unseen):
        messages_list = []
        for email_bytes, uid in zip(data, uid_list):
            is_unseen = True if unseen.find(uid) >= 0 else False
            mail = email.message_from_bytes(email_bytes[1], policy=policy.default)
            mail_info_dict = {'uid': uid, 'from': mail['From'], 'to': mail['To'],
                              'subject': mail['Subject'], 'unseen': is_unseen}
            messages_list.append(mail_info_dict)
        messages_list.reverse()
        return messages_list
