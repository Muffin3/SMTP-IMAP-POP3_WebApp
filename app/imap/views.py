from . import imap_blueprint as imap
from flask import redirect, render_template, request, session, url_for, send_file
from app.pagination import Pagination
from app.services import my_imap


@imap.route('/<string:mailbox>/page/<int:page>/', methods=['GET'])
@imap.route('/<string:mailbox>/', defaults={'page': 1}, methods=['GET'])
@imap.route('/', defaults={'mailbox': 'inbox', 'page': 1}, methods=['GET'])
def index(mailbox, page):
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    per_page = 20
    imap_obj = my_imap.MyIMAP(session['mailbox'][0], session['mailbox'][1])
    total, mail_list, mailboxes = imap_obj.messages_list(page, per_page, mailbox)
    pagination = Pagination(page, per_page, total)
    return render_template('imap/index.html', mail_list=mail_list, errors=imap_obj.errors, protocol='imap',
                           mailbox=mailbox, mailboxes=mailboxes, pagination=pagination)


@imap.route('/<string:mailbox>/mail/<int:uid>/', methods=['GET'])
def readmail(mailbox, uid):
    imap_obj = my_imap.MyIMAP(session['mailbox'][0], session['mailbox'][1])
    message = imap_obj.read_msg(mailbox, uid)
    return render_template('imap/readmail.html', mailbox=mailbox, message=message)


@imap.route('/<string:mailbox>/mark/seen/', methods=['GET', 'POST'])
def mark_seen(mailbox):
    if request.method == 'POST':
        imap_obj = my_imap.MyIMAP(session['mailbox'][0], session['mailbox'][1])
        imap_obj.mark_seen(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('imap.index', mailbox=mailbox), 302)


@imap.route('/<string:mailbox>/mark/unseen/', methods=['GET', 'POST'])
def mark_unseen(mailbox):
    if request.method == 'POST':
        imap_obj = my_imap.MyIMAP(session['mailbox'][0], session['mailbox'][1])
        imap_obj.mark_unseen(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('imap.index', mailbox=mailbox), 302)


@imap.route('/<string:mailbox>/mark/deleted/', methods=['GET', 'POST'])
def mark_deleted(mailbox):
    if request.method == 'POST':
        imap_obj = my_imap.MyIMAP(session['mailbox'][0], session['mailbox'][1])
        imap_obj.mark_deleted(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('imap.index', mailbox=mailbox), 302)


@imap.route('/<string:mailbox>/download/<int:uid>/<string:filename>', methods=['GET'])
def download(mailbox, filename, uid):
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    imap_obj = my_imap.MyIMAP(session['mailbox'][0], session['mailbox'][1])
    file = imap_obj.download(mailbox, filename, uid)
    return send_file(file, attachment_filename=filename, as_attachment=True)
