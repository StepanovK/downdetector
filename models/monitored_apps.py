from db import db
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
        return {
            "id": self.id,
            "name": self.name,
            "checking_interval": self.checking_interval,
            "checking_is_active": self.checking_is_active,
            "logs": [log.json() for log in self.logs],
            "status_checks": [status_check.json() for status_check in self.status_checks.order_by('date').limit(100)],
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
            self.token_hash = hashlib.sha224(token.encode()).hexdigest()
        db.session.add(self)
        db.session.commit()
        return token

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def check_token(self, token: str):
        return secrets.compare_digest(self.token_hash, token.encode())
