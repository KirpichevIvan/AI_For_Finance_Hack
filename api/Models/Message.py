from database import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(2048), unique=False)
    time = db.Column(db.DateTime, unique=False)
    type = db.Column(db.Boolean) # 0 - text, 1 - audio
    code = db.Column(db.String(4), unique=False)
    sender = db.Column(db.Boolean) # 0 - user, 1 - server


    def __init__(self, message, time, type, code, sender):  
        self.message = message 
        self.time = time
        self.type = type
        self.code = code 
        self.sender = sender

    def __repr__(self):
        return '<Message %r>' % self.message
