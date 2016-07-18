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
your [Authy API key](https://dashboard.authy.com)
your [Twilio API key]
your [SECRET_KEY]

1. Run `source secrets.sh` to apply the environment variables
