from app.models import db
from datetime import datetime

class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_shared = db.Column(db.Boolean, default=False)
    share_code = db.Column(db.String(50), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('ItineraryItem', backref='itinerary', lazy=True, cascade="all, delete-orphan")

    @classmethod
    def create(cls, **kwargs):
        itinerary = cls(**kwargs)
        db.session.add(itinerary)
        db.session.commit()
        return itinerary

    @classmethod
    def get_by_id(cls, itinerary_id):
        return cls.query.get(itinerary_id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ItineraryItem(db.Model):
    __tablename__ = 'itinerary_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=True)
    day_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    expected_cost = db.Column(db.Numeric(10, 2), default=0)
    note = db.Column(db.Text, nullable=True)

    @classmethod
    def create(cls, **kwargs):
        item = cls(**kwargs)
        db.session.add(item)
        db.session.commit()
        return item

    def delete(self):
        db.session.delete(self)
        db.session.commit()
