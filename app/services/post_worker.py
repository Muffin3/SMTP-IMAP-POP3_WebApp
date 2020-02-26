from . import my_imap


class PostWorker:
    def __init__(self, protocol='imap'):
        self.protocol = self.protocols(protocol)()

    def protocols(self, name):
        return {'imap': my_imap.MyIMAP}.get(name)

    def connect(self, *args):
        return self.protocol.connect(args[0], args[1])

    def messages_list(self, page, per_page, mailbox):
        return self.protocol.messages_list(page, per_page, mailbox)

    def mailboxes_list(self):
        return self.protocol.mailboxes_list()

    def read_msg(self, mailbox, uid):
        return self.protocol.read_msg(mailbox, uid)

    def mark_seen(self, uid_list, mailbox):
        return self.protocol.mark_seen(uid_list, mailbox)

    def mark_unseen(self, uid_list, mailbox):
        return self.protocol.mark_unseen(uid_list, mailbox)

    def mark_deleted(self, uid_list, mailbox):
        return self.protocol.mark_deleted(uid_list, mailbox)
    @property
    def errors(self):
        return self.protocol.errors
