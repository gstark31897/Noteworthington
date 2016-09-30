from Noteworthington import app

from flask_login import current_user

import random
from bson.objectid import ObjectId

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SettingsForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField()


class Note():
    def __init__(self, id):
        self.id = id

    @property
    def title(self):
        return app.config['NOTES_COLLECTION'].find_one({'_id': self.id}, projection=['title'])['title']

    @property
    def text(self):
        return app.config['NOTES_COLLECTION'].find_one({'_id': self.id}, projection=['text'])['text']

    def rename(self, new_name):
        app.config['NOTES_COLLECTION'].update({'_id': self.id}, {'$set': {'title': new_name}})

    def edit(self, new_text):
        app.config['NOTES_COLLECTION'].update({'_id': self.id}, {'$set': {'text': new_text}})

    def delete(self):
        app.config['NOTES_COLLECTION'].remove({'_id': self.id})

    @staticmethod
    def create_note(owner):
        return app.config['NOTES_COLLECTION'].insert({'owner': owner, 'title': 'Untitled', 'text': ''})

def list_notes():
    return [Note(note['_id']) 
        for note in app.config['NOTES_COLLECTION'].find({'owner': current_user.username}, projection=['_id'])]
    #return [Note("Note %s" % i, current_user.username) for i in range(20)]


def get_note(id):
    note = app.config['NOTES_COLLECTION'].find_one({'owner': current_user.username, '_id': ObjectId(id)}, projection=['_id'])
    return Note(note['_id'])


def create_note():
    return str(Note.create_note(current_user.username))


def update_settings(id, form):
    note = get_note(id)
    note.rename(form.title.data)


def update_note(id, data):
    note = get_note(id)
    note.edit(data['text'])


def delete_note(id):
    note = get_note(id)
    note.delete()

