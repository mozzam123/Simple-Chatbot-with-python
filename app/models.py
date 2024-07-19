from . import db
from sqlalchemy.dialects.mysql import JSON
import datetime

class OpenAPIChatbot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_userid = db.Column(db.Integer, nullable=False)
    urls = db.Column(JSON, nullable=False)
    botname = db.Column(db.String(100), nullable=False)
    vectorstore = db.Column(db.LargeBinary, nullable=False)


    def __repr__(self):
        return f'<OpenAPIChatbot {self.botname} {self.customer_userid}>'

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer,nullable=False)
    customer_userid = db.Column(db.Integer, nullable=False)
    sender= db.Column(db.String(500), nullable=False)
    user_message = db.Column(db.String(500), nullable=False)
    bot_response = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<ChatHistory {self.customer_userid} {self.timestamp}>'
    
class Customers(db.Model):
    __table__ = db.Table('Customers', db.metadata, autoload_with=db.engine)

