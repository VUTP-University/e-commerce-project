import uuid
from extensions import db


class Inventory(db.Model):
    __tablename__ = 'users'
    product_id = db.Column(db.String(256), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    quantity = db.Column(db.Number(10), unique=False, nullable=False)
    reserved = db.Column(db.Boolean(10), unique=False, nullable=False)
