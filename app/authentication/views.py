from . import auth_blueprint as auth
from flask import redirect, render_template, request, session, url_for
from .forms import authentication
from app.services import my_pop3


@auth.route('/', methods=['GET', 'POST'])
def index():
    if 'mailbox' in session:
        return redirect('/', 302)
    form = authentication.Authentication(request.form)
    errors = ()
    if request.method == 'POST':
        imap_obj = my_pop3.MyPOP3(form.mailbox.data, form.password.data)
        if form.validate() and imap_obj.get_connect():
            session['mailbox'] = (form.mailbox.data, form.password.data)
            return redirect(url_for('imap.index'), 302)
        errors = imap_obj.errors
    return render_template('authentication/auth.html', form=form, errors=errors)


@auth.route('/logout/')
def logout():
    if 'mailbox' in session:
        session.pop('mailbox')
    return redirect(url_for('auth.index'), 302)
