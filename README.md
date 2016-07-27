### Gigaware dev guide

This project is built using the [Flask](http://flask.pocoo.org/) web framework.
It runs on Python 2.7 or 3.4+.

1. To run the app locally, first clone this repository and `cd` into it.

1. Create a new virtual environment.

    - If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```
        virtualenv venv
        source venv/bin/activate
        ```

1. Install the requirements.

    ```
    pip install -r requirements.txt
    ```

1. Copy the `.env_example` file to `secrets.sh`, and edit it to include:
    - your [TWILIO_AUTH_TOKEN]
    - your [Twilio API key]
    - your [TWILIO_NUMBER]
    - your [TWILIO_ACCOUNT_SID]
    - your [SECRET_KEY]
    - your [DATABASE_URL]

1. Run `source secrets.sh` to apply the environment variables

1. Run the postgresql server
1. Create the gigaware database in your local enviornment
    - run `psql gigaware` to verify that the db doesn't already exist
    - `createdb gigaware`
    - `db.create_all()`

1. Run `python manage.py db upgrade` to build migration models for the db and `python manage.py db downgrade` to drop the tables

1. Run `python manage.py runserver` to start the app
