from db import db


class ApplicationLog(db.Model):
    __tablename__ = 'app_logs'

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), nullable=False)
    date = db.Column(db.DateTime)
    short_message = db.Column(db.String(255))
    message = db.Column(db.Text)
    level = db.Column(db.Integer)  # 0 - info, 1 - warning, 2 - error

    def json(self):
        return {
            "app_id": self.app,
            "date": self.date,
            "short_message": self.short_message,
            "message": self.message,
            "level": self.level,
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
