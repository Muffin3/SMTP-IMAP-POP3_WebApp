from . import imap_blueprint as imap
from flask import redirect, render_template, request, session, url_for, send_file
from .pagination import Pagination
from app.services import post_worker
import io


@imap.route('/<string:mailbox>/page/<int:page>/', methods=['GET'])
@imap.route('/<string:mailbox>/', defaults={'page': 1}, methods=['GET'])
@imap.route('/', defaults={'mailbox': 'inbox', 'page': 1}, methods=['GET'])
def index(mailbox, page):
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    total, per_page, mail_list, mailboxes, pagination = 0, 20, [], [], None
    post = post_worker.PostWorker()
    if post.connect(session['mailbox'][0], session['mailbox'][1]):
        total, mail_list, mailboxes = post.messages_list(page, per_page, mailbox)
        pagination = Pagination(page, per_page, total)
    return render_template('imap/index.html', mail_list=mail_list, errors=post.errors, protocol='imap', mailbox=mailbox,
                           mailboxes=mailboxes, pagination=pagination)


@imap.route('/<string:mailbox>/mail/<int:uid>/', methods=['GET'])
def mail(mailbox, uid):
    message = dict()
    post = post_worker.PostWorker()
    if post.connect(session['mailbox'][0], session['mailbox'][1]):
        message = post.read_msg(mailbox, uid)
    return render_template('mail.html', protocol='imap', mailbox=mailbox, message=message)


@imap.route('/<string:protocol>/<string:mailbox>/mark/seen/', methods=['GET', 'POST'])
def mark_seen(protocol, mailbox):
    if request.method == 'POST':
        post = post_worker.PostWorker(protocol)
        if post.connect(session['mailbox'][0], session['mailbox'][1]):
            post.mark_seen(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('index', protocol=protocol, mailbox=mailbox), 302)


@imap.route('/<string:protocol>/<string:mailbox>/mark/unseen/', methods=['GET', 'POST'])
def mark_unseen(protocol, mailbox):
    if request.method == 'POST':
        post = post_worker.PostWorker(protocol)
        if post.connect(session['mailbox'][0], session['mailbox'][1]):
            post.mark_unseen(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('index', protocol=protocol, mailbox=mailbox), 302)


@imap.route('/<string:protocol>/<string:mailbox>/mark/deleted/', methods=['GET', 'POST'])
def mark_deleted(protocol, mailbox):
    if request.method == 'POST':
        post = post_worker.PostWorker(protocol)
        if post.connect(session['mailbox'][0], session['mailbox'][1]):
            post.mark_deleted(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('index', protocol=protocol, mailbox=mailbox), 302)


@imap.route('/logout/')
def logout():
    if 'mailbox' in session:
        session.pop('mailbox')
    return redirect('/auth/', 302)


@imap.route('/download/')
def look():
    file = io.BytesIO()
    file.write(b'Hello World')
    file.seek(0)
    return send_file(file, attachment_filename='file.txt', as_attachment=True, cache_timeout=-1)
