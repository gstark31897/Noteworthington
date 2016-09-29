from Noteworthington import app

from flask_login import current_user

import random


class Note():
    def __init__(self, title, owner):
        self.title = title
        self.owner = owner

    @property
    def preview(self):
        text = 'some preview text that will never be used (should have used Lorem Ipsum)'
        for i in range(random.randint(0, 4)):
            text += text
        return text

def list_notes():
    return [Note("Note %s" % i, current_user.username) for i in range(20)]
