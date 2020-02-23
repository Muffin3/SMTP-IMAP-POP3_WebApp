from app import app
from flask import redirect, render_template, request, session, url_for
from pagination import Pagination
from forms import authentication
from services import post_worker


@app.route('/<string:protocol>/<string:mailbox>/page/<int:page>/', methods=['GET'])
@app.route('/<string:protocol>/<string:mailbox>/', defaults={'page': 1}, methods=['GET'])
@app.route('/<string:protocol>/', defaults={'mailbox': 'inbox', 'page': 1}, methods=['GET'])
@app.route('/', defaults={'protocol': 'imap', 'mailbox': 'inbox', 'page': 1}, methods=['GET'])
def index(protocol, mailbox, page):
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    total, per_page, mail_list, mailboxes, pagination = 0, 20, [], [], None
    post = post_worker.PostWorker(protocol)
    if post.connect(session['mailbox'][0], session['mailbox'][1]):
        total, mail_list, mailboxes = post.messages_list(page, per_page, mailbox)
        pagination = Pagination(page, per_page, total)
    return render_template('index.html', mail_list=mail_list, errors=post.errors, protocol=protocol, mailbox=mailbox,
                           mailboxes=mailboxes, pagination=pagination)


@app.route('/<string:protocol>/<string:mailbox>/mail/<int:uid>/', methods=['GET'])
def mail(protocol, mailbox, uid):
    mail, body = '', ''
    post = post_worker.PostWorker(protocol)
    if post.connect(session['mailbox'][0], session['mailbox'][1]):
        mail, body = post.read_msg(mailbox, uid)
    return render_template('mail.html', protocol=protocol, mailbox=mailbox, mail=mail, body=body)


@app.route('/<string:protocol>/<string:mailbox>/mark/seen/', methods=['GET', 'POST'])
def mark_seen(protocol, mailbox):
    if request.method == 'POST':
        post = post_worker.PostWorker(protocol)
        if post.connect(session['mailbox'][0], session['mailbox'][1]):
            post.mark_seen(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('index', protocol=protocol, mailbox=mailbox), 302)


@app.route('/<string:protocol>/<string:mailbox>/mark/unseen/', methods=['GET', 'POST'])
def mark_unseen(protocol, mailbox):
    if request.method == 'POST':
        post = post_worker.PostWorker(protocol)
        if post.connect(session['mailbox'][0], session['mailbox'][1]):
            post.mark_unseen(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('index', protocol=protocol, mailbox=mailbox), 302)


@app.route('/<string:protocol>/<string:mailbox>/mark/deleted/', methods=['GET', 'POST'])
def mark_deleted(protocol, mailbox):
    if request.method == 'POST':
        post = post_worker.PostWorker(protocol)
        if post.connect(session['mailbox'][0], session['mailbox'][1]):
            post.mark_deleted(request.form.getlist('mail_ids'), mailbox)
    return redirect(url_for('index', protocol=protocol, mailbox=mailbox), 302)


@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    if 'mailbox' in session:
        return redirect('/', 302)
    form = authentication.Authentication(request.form)
    post = post_worker.PostWorker('imap')
    if request.method == 'POST':
        if form.validate() and post.connect(form.mailbox.data, form.password.data):
            session['mailbox'] = (form.mailbox.data, form.password.data)
            return redirect('/', 302)
    return render_template('auth.html', form=form, errors=post.errors)


@app.route('/logout/')
def logout():
    if 'mailbox' in session:
        session.pop('mailbox')
    return redirect('/auth/', 302)


@app.route('/file')
def look():
    return redirect(url_for('static', filename='lab1.docx'))
