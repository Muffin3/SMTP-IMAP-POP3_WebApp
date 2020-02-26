from . import auth_blueprint as auth
from flask import redirect, render_template, request, session, url_for
from .forms import authentication
from app.services import my_imap


@auth.route('/', methods=['GET', 'POST'])
def index():
    if 'mailbox' in session:
        return redirect('/', 302)
    form = authentication.Authentication(request.form)
    imap_obj = my_imap.MyIMAP()
    if request.method == 'POST':
        if form.validate() and imap_obj.connect(form.mailbox.data, form.password.data):
            session['mailbox'] = (form.mailbox.data, form.password.data)
            return redirect('/', 302)
    return render_template('authentication/auth.html', form=form, errors=imap_obj.errors)


@auth.route('/logout/')
def logout():
    if 'mailbox' in session:
        session.pop('mailbox')
    return redirect(url_for('auth.index'), 302)
