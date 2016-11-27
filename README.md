# Two-Factor Authentication with Authy OneTouch

This application example demonstrates how to implement Two-Factor Authentication on a Python Flask application using [Authy OneTouch](https://www.authy.com/developers/).

## Quickstart

### Create an Authy app

Create a free [Authy account](https://www.authy.com/developers/) if you haven't
already done so and then connect it to your Twilio account.

Create a new Authy application. Be sure to set the OneTouch callback
endpoint to `http://your-server-here.com/authy/callback` once you've finished
configuring the app.

### Local development

This project is built using the [Flask](http://flask.pocoo.org/) web framework.
For now it only runs on Python 2.7 (not 3.4+).

1. To run the app locally, first clone this repository and `cd` into it.

1. Create a new virtual environment.

    - If using [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```
        pip install virtualenv
        virtualenv two-factor-env
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```
        mkvirtualenv two-factor-env
        ```

1. Install the requirements.

    ```
    pip install -r requirements.txt
    ```

1. Run the migrations.

    ```
    python manage.py migrate
    ```

1. Start the development server.

    ```
    python manage.py runserver
    ```

To actually process OneTouch authentication requests, your development server will need to be publicly accessible. [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).

Once you have started ngrok, set your Authy app's OneTouch callback URL to use your ngrok hostname, like this:

```
http://88b37ada.ngrok.io/authy/callback
```