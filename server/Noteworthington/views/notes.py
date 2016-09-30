from Noteworthington import app
from Noteworthington.models import notes as notes_model

from flask import render_template, redirect, request
from flask_login import login_required


@app.route('/notes')
@login_required
def notes():
    notes = notes_model.list_notes()
    return render_template('notes.html', notes=notes)


@app.route('/notes/<id>')
@login_required
def get_note(id):
    note = notes_model.get_note(id)
    return render_template('note.html', note=note)


@app.route('/notes/create_note')
@login_required
def create_note():
    id = notes_model.create_note()
    return redirect('/notes/' + id)


@app.route('/notes/<id>/settings', methods=['GET', 'POST'])
@login_required
def note_settings(id):
    form = notes_model.SettingsForm()
    if form.validate_on_submit():
        notes_model.update_settings(id, form)
        return redirect('/notes/' + id)
    note = notes_model.get_note(id)
    form.title.data = note.title
    return render_template('note_settings.html', note=note, form=form)

@app.route('/notes/<id>/update_note', methods=['POST'])
@login_required
def update_note(id):
    notes_model.update_note(id, request.form)
    return 'Success'


@app.route('/notes/<id>/delete')
@login_required
def delete_note(id):
    notes_model.delete_note(id)
    return redirect('/notes')
