from db import db


class ApplicationStatusCheck(db.Model):
    __tablename__ = 'app_status_checks'

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), nullable=False)
    date = db.Column(db.DateTime)

    def json(self):
        return {
            'id': self.id,
            'app': self.app_id,
            'date': self.date,
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
