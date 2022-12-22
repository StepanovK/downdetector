from .extensions import db
from .status_cheks import ApplicationStatusCheck
from .app_logs import ApplicationLog
import secrets
import hashlib


class MonitoredApp(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    checking_interval = db.Column(db.Integer)
    checking_is_active = db.Column(db.Boolean)
    token_hash = db.Column(db.String(255))

    logs = db.relationship('ApplicationLog', backref='app', lazy='dynamic')
    status_checks = db.relationship('ApplicationStatusCheck', backref='app', lazy='dynamic')
    user_subscribes = db.relationship('UserSubscribe', backref='app', lazy='dynamic')

    def json(self):
        status_checks = self.status_checks.order_by(ApplicationStatusCheck.date.desc()).limit(1)
        logs = self.logs.order_by(ApplicationLog.date.desc()).limit(500)
        return {
            "id": self.id,
            "name": self.name,
            "checking_interval": self.checking_interval,
            "checking_is_active": self.checking_is_active,
            "logs": [log.json() for log in logs],
            "last_activity": 0 if status_checks.count() == 0 else status_checks[0].date.timestamp(),
        }

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self, generate_token=True):
        token = None
        if generate_token:
            token = secrets.token_urlsafe(16)
            self.token_hash = self.get_token_hash(token)
        db.session.add(self)
        db.session.commit()
        return token

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_token(self, token: str):
        return secrets.compare_digest(self.token_hash, self.get_token_hash(token))

    @classmethod
    def get_token_hash(cls, token: str) -> str:
        return hashlib.sha224(token.encode()).hexdigest()
