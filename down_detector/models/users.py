from .extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(150), default='')
    first_name = db.Column(db.String(150), default='')
    last_name = db.Column(db.String(150), default='')
    telegram_id = db.Column(db.Integer, nullable=True)

    subscribes = db.relationship('UserSubscribe', backref='user', lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'login': self.login,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'telegram_id': self.telegram_id,
            'subscribes': [subscribe.json() for subscribe in self.subscribes],
        }

    @classmethod
    def get_by_telegram_id(cls, telegram_id):
        return cls.query.filter_by(telegram_id=telegram_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
