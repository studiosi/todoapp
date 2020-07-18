from datetime import datetime, timezone
from . import db


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    active = db.Column(db.Boolean, nullable=False, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)
    items = db.relationship('Item')

    def __init__(self, name):
        self.name = name

    def add_item(self, item):
        self.items.append(item)


