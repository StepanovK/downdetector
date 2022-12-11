from db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    telegram_id = db.Column(db.Integer)

    subscribes = db.relationship('UserSubscribe', backref='user', lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'telegram_id': self.tg_id,
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
