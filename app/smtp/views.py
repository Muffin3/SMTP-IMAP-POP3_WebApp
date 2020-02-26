from werkzeug.datastructures import CombinedMultiDict
from . import smtp_blueprint as smtp
from flask import redirect, render_template, request, session, url_for
from app.smtp.forms.new_mail import NewMail
from app.services import my_smtp


@smtp.route('/new/', methods=['GET', 'POST'])
def new_mail():
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    new_mail_form = NewMail(CombinedMultiDict((request.files, request.form)))
    smtp_obj = my_smtp.MySMTP(session['mailbox'][0], session['mailbox'][1])
    if request.method == 'POST':
        if smtp_obj.send(new_mail_form):
            session['Notify'] = ('Сообщение отправлено!', )
            return redirect(url_for('imap.index', mailbox='sent'), 302)
    return render_template('smtp/newmail.html', new_mail_form=new_mail_form, errors=smtp_obj.errors)
