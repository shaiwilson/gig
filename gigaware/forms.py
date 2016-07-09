from flask_wtf import Form
from wtforms import TextField, PasswordField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, URL


class RegisterForm(Form):
    name = TextField(
            'Tell us your name:',
            validators=[DataRequired(message="Name is required"),
                        Length(min=3, message="Name must greater than 3 chars")]
    )
    email = TextField(
            'Enter your E-mail:',
            validators=[DataRequired("E-mail is required"), Email(message="Invalid E-mail address")]
    )
    password = PasswordField(
            'Password:',
            validators=[DataRequired("Password is required")]
    )
    country_code = TextField(
            'Country Code:',
            validators=[DataRequired("Country code is required"),
                        Length(min=1, max=4, message="Country code must be between 1 and 4 numbers")]
    )

    phone_number = IntegerField(
            'Phone Number:',
            validators=[DataRequired("Valid phone number is required")]
    )

    zip_code = IntegerField(
            'Post code:',
            validators=[DataRequired("Valid postcode is required")]
    )


class LoginForm(Form):
    email = TextField(
            'E-mail:',
            validators=[DataRequired("E-mail is required"), Email(message="Invalid E-mail address")]
    )
    password = PasswordField(
            'Password:',
            validators=[DataRequired("Password is required")]
    )

class JobListingForm(Form):
    description = TextField(
            'Job Task:',
            validators=[DataRequired("Description is required")]
    )
    image_url = TextField(
            'Image URL:',
            validators=[DataRequired("Image Url required"), URL(message="Invalid Image Url")]
    )
    city = TextField(
            'City:',
            validators=[DataRequired("City required")]
    )
    country = TextField(
            'Country:',
            validators=[DataRequired("Country required")]
    )
    zip_code = TextField(
            'Zip code:',
            validators=[DataRequired("Zip code required")]
    )
    details = TextField(
            'Description:'
    )
    price = TextField(
            'Price:',
            validators=[DataRequired("Price required")]
    )
    currency = TextField(
            'Currency:',
            validators=[DataRequired("Currency required")]
    )


class ApplicationForm(Form):
    message = TextField(
            'Message:',
            validators=[DataRequired("Message is required")]
    )

    property_id = HiddenField()


class ApplicationConfirmationForm(Form):
    From = TextField('From')
    Body = TextField('Body')


class ExchangeForm(Form):
    From = TextField('From')
    To = TextField('To')
    Body = TextField('Body')
