from datetime import datetime, timedelta
from database import db

class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_revoked = db.Column(db.Boolean, default=False)

    def __init__(self, token, user_id, expires_in_days=7):
        self.token = token
        self.user_id = user_id
        self.expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

    def __repr__(self):
        return f'<RefreshToken {self.token}>'