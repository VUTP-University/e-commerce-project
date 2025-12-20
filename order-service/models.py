import uuid
from extensions import db


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=False)
    products = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    modified_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    def __init__(self, user_id, products, status='pending'):
        self.user_id = user_id
        self.products = products
        self.status = status
        

