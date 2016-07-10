from gigaware.models import app_db

db = app_db()


class JobTask(db.Model):
    __tablename__ = "job_listings"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)

    host_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    host = db.relationship("User", back_populates="job_listings")
    reservations = db.relationship("Reservation", back_populates="job_task")

    def __init__(self, description, image_url, city, country, zip_code,
                    details, price, currency, host):
        self.description = description
        self.image_url = image_url
        self.city = city
        self.country = country
        self.zip_code = zip_code
        self.details = details
        self.price = price
        self.currency = currency
        self.host = host

    def __repr__(self):
        return '<Task {0} {1}>'.format(self.id, self.description)
