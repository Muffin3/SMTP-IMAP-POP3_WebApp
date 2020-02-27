from . import pop3_blueprint as pop3
from flask import redirect, render_template, request, session, url_for, send_file
from app.pagination import Pagination
from app.services import my_pop3


@pop3.route('/page/<int:page>/', methods=['GET'])
@pop3.route('/', defaults={'page': 1}, methods=['GET'])
def index(page):
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    per_page, mail_list, pagination = 20, [], None
    pop3_obj = my_pop3.MyPOP3(session['mailbox'][0], session['mailbox'][1])
    total, mail_list = pop3_obj.get_messages_list(page, per_page)
    pagination = Pagination(page, per_page, total)
    return render_template('pop3/index.html', mail_list=mail_list, errors=pop3_obj.errors, protocol='pop3',
                           pagination=pagination)


@pop3.route('/mail/<int:mid>/', methods=['GET'])
def readmail(mid):
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    pop3_obj = my_pop3.MyPOP3(session['mailbox'][0], session['mailbox'][1])
    message = pop3_obj.get_message(mid)
    return render_template('pop3/readmail.html', message=message, errors=pop3_obj.errors)


@pop3.route('/mark/deleted/', methods=['GET', 'POST'])
def mark_deleted():
    if request.method == 'POST':
        pop3_obj = my_pop3.MyPOP3(session['mailbox'][0], session['mailbox'][1])
        pop3_obj.delete_message(request.form.getlist('mail_ids'))
    return redirect(url_for('pop3.index'), 302)


@pop3.route('/download/<int:uid>/<string:filename>', methods=['GET'])
def download(filename, uid):
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    pop3_obj = my_pop3.MyPOP3(session['mailbox'][0], session['mailbox'][1])
    file = pop3_obj.download(filename, uid)
    return send_file(file, attachment_filename=filename, as_attachment=True)
