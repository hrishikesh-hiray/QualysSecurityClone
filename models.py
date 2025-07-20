from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    scans = db.relationship('SecurityScan', backref='user', lazy=True)

class SecurityScan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_type = db.Column(db.String(20), nullable=False)  # 'was' or 'iac'
    target = db.Column(db.String(500), nullable=False)  # URL or filename
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    results = db.Column(db.Text)  # JSON string of results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    author = db.Column(db.String(100), default='CyferTrace Team')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(50), default='Security')
