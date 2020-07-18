from datetime import datetime, timezone
from . import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    active = db.Column(db.Boolean, nullable=False, default=True)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def __init__(self, content, order):
        self.content = content
        self.order = order

    def logical_delete(self):
        self.active = False
        self.order = -1
        self.deleted_at = datetime.now(timezone.utc)
