from Noteworthington import app
from Noteworthington.views import login, notes

from flask import render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, View


nav = Nav()


@nav.navigation()
def navbar():
    return Navbar(
        'Noteworthington',
        View('Home', 'index'),
        View('Notes', 'notes'),
        View('Login', 'login'),
    )


@app.route('/')
def index():
    return render_template('index.html')


nav.init_app(app)
