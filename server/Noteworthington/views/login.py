from Noteworthington import app
from Noteworthington.models import login as login_model

from flask import render_template, redirect, request
from flask_login import login_required, logout_user


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = login_model.LoginForm()
    if form.validate_on_submit():
        if login_model.login(form):
            return redirect(request.args.get("next") or '/')
    return render_template('login.html', form=form)


@app.route('/test')
@login_required
def test():
    return 'Test'


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

