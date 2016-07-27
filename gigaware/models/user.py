from gigaware.models import app_db
from gigaware.models import bcrypt

from flask_sqlalchemy import SQLAlchemy
from gigaware import db

db = app_db()
bcrypt = bcrypt()

##############################################################################
# Model definitions

class User(db.Model):
    """
    Represents a single user in the system.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(30), nullable=False)
    area_code = db.Column(db.String(15), nullable=True) # telephone
    zip_code = db.Column(db.Integer, nullable=True)  # address

    reservations = db.relationship("Reservation", back_populates="guest")
    job_listings = db.relationship("JobTask", back_populates="host")

    def __init__(self, first_name, last_name, email, password,
                phone_number, area_code, zip_code):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.phone_number = phone_number
        self.area_code = area_code
        self.zip_code = zip_code

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    # Python 3

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<User %r>' % (self.name)
