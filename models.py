from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Organisation(db.Model):
    org_id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(100), nullable=False)
    org_address = db.Column(db.String(255))
    org_contact = db.Column(db.String(20))
    admins = db.relationship('Admin', backref='organisation', lazy=True)
    services = db.relationship('Service', backref='organisation', lazy=True)

class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Use appropriate hashing for real-world scenarios
    profile_picture = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.org_id'), nullable=False)
    
    def get_id(self):
        return str(self.admin_id)

class Service(db.Model):
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.org_id'), nullable=False)
    queues = db.relationship('Queue', backref='service', lazy=True)

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Use appropriate hashing for real-world scenarios
    profile_picture = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

class Queue(db.Model):
    queue_id = db.Column(db.Integer, primary_key=True)
    queue_number = db.Column(db.Integer, nullable=False)
    time_passed = db.Column(db.Time)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    admin_id =  db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    status = db.Column(db.Enum('Queuing', 'Served'), nullable=False)

# Add any additional models or relationships as needed
