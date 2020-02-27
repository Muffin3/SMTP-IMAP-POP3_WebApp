import base64
import email
import io
import re
from email import policy
import poplib


class MyPOP3:
    def __init__(self, address, password):
        self.address = address
        self.password = password
        self.server_name = 'pop.' + self.address[self.address.find('@') + 1:]
        self.errors = None

    def get_connect(self):
        try:
            pop3 = poplib.POP3_SSL(self.server_name, 995)
            pop3.user(self.address)
            pop3.pass_(self.password)
            return pop3
        except poplib.error_proto:
            self.errors = ('Ошибка авторизации!', )

    def get_messages_list(self, page, per_page):
        total, mail_list = 0, []
        pop3 = self.get_connect()
        if pop3:
            resp, msgs, oct = pop3.list()
            total = len(msgs)
            start, end = self.get_msg_num_by_page(page, per_page, total)
            for msg_num in range(start, end, -1):
                resp, msg_bytes, oct = pop3.retr(msg_num)
                msg_byte_str = b'\n'.join(msg_bytes)
                email_obj = email.message_from_bytes(msg_byte_str, policy=policy.default)
                mail_list.append({'id': msg_num, 'From': email_obj['From'], 'To': email_obj['To'],
                                  'Subject': email_obj['Subject']})
        return total, mail_list

    def get_message(self, mid):
        pop3 = self.get_connect()
        if pop3:
            resp, msg_bytes, oct = pop3.retr(mid)
            msg_byte_str = b'\n'.join(msg_bytes)
            email_obj = email.message_from_bytes(msg_byte_str, policy=policy.default)
            content = self.get_body(email_obj).decode('utf-8')
            content = re.sub('\r\n', '<br>', content) if content.find('<head>') < 0 else content
            message = {'id': mid, 'From': email_obj['From'], 'To': email_obj['To'], 'Subject': email_obj['Subject'],
                       'Content': content, 'Attachments': []}
            for part in email_obj.walk():
                if part.get_filename():
                    message['Attachments'].append(part.get_filename())
            return message

    def delete_message(self, mid_list):
        pop3 = self.get_connect()
        if pop3:
            for mid in mid_list:
                print(pop3.dele(mid))
            pop3.quit()

    def download(self, filename, mid):
        file = io.BytesIO()
        pop3 = self.get_connect()
        if pop3:
            resp, msg_bytes, oct = pop3.retr(mid)
            msg_byte_str = b'\n'.join(msg_bytes)
            email_obj = email.message_from_bytes(msg_byte_str, policy=policy.default)
            for part in email_obj.walk():
                if part.get_filename() == filename:
                    file.write(part.get_payload(decode=True))
                    file.seek(0)
                    break
            return file

    def get_msg_num_by_page(self, page, per_page, total):
        start = total - (page-1) * per_page
        end = start - 21
        end = 0 if end < 0 else end
        return start, end

    def get_body(self, msg):
        if msg.is_multipart():
            return self.get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, decode=True)
