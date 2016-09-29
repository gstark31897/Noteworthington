from Noteworthington import app
from Noteworthington.models import notes as notes_model

from flask import render_template, redirect, request
from flask_login import login_required


@app.route('/notes')
@login_required
def notes():
    notes = notes_model.list_notes()
    return render_template('notes.html', notes=notes)

