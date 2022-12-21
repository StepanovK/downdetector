from .extensions import db


class UserSubscribe(db.Model):
    __tablename__ = 'user_subscribes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), nullable=False)
    token = db.Column(db.String(255))

    def json(self):
        return {
            'user': self.user_id,
            'app': self.app_id,
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
