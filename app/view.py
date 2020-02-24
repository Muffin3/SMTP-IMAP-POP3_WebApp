from . import app
from flask import redirect, session, url_for


@app.route('/')
def index():
    if 'mailbox' not in session:
        return redirect('/auth/', code=302)
    return redirect(url_for('imap.index'), 302)
