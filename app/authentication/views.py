from . import auth_blueprint as auth
from flask import redirect, render_template, request, session, url_for, send_file
from .forms import authentication
from app.services import post_worker
import io


@auth.route('/', methods=['GET', 'POST'])
def index():
    if 'mailbox' in session:
        return redirect('/', 302)
    form = authentication.Authentication(request.form)
    post = post_worker.PostWorker('imap')
    if request.method == 'POST':
        if form.validate() and post.connect(form.mailbox.data, form.password.data):
            session['mailbox'] = (form.mailbox.data, form.password.data)
            return redirect('/', 302)
    return render_template('authentication/auth.html', form=form, errors=post.errors)


@auth.route('/logout/')
def logout():
    if 'mailbox' in session:
        session.pop('mailbox')
    return redirect('/auth/', 302)


@auth.route('/download/')
def look():
    file = io.BytesIO()
    file.write(b'Hello World')
    file.seek(0)
    return send_file(file, attachment_filename='file.txt', as_attachment=True, cache_timeout=-1)
