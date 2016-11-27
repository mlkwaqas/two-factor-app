from authy.api import AuthyApiClient
from django.contrib.auth.models import User
import requests
from Authapp.settings import AUTHY_API_KEY
from authentication.models import UserProfile


def get_authy_client():
    """Returns an AuthyApiClient"""
    return AuthyApiClient(AUTHY_API_KEY)


def create_user_profile(data, authy_user):
    user = User.objects.create_user(
        email=data.get('email'),
        username=data.get('email'),
        password=data.get('password'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
    )
    UserProfile.objects.create(
        user=user,
        phone_number=data.get('phone_number'),
        country_code=data.get('country_code'),
        authy_id=authy_user.id
    )


def create_authy_user(form):
    data = {
        'email': form.cleaned_data['email'],
        'first_name': form.cleaned_data['first_name'],
        'last_name': form.cleaned_data['last_name'],
        'password': form.cleaned_data['password'],
        'phone_number': form.cleaned_data['phone_number'],
        'country_code': form.cleaned_data['country_code'],
    }

    authy_client = get_authy_client()
    authy_user = authy_client.users.create(data.get('email'), data.get('phone_number'), data.get('country_code'))

    if authy_user.ok():
        create_user_profile(data, authy_user)


def send_one_touch_request(user):

    authy_client = get_authy_client()

    url = '{0}/onetouch/json/users/{1}/approval_requests'.format(authy_client.api_uri, user.profile.authy_id)
    data = {
        'api_key': authy_client.api_key,
        'message': 'Request to log in to Twilio demo app',
        'details[Email]': user.email
    }
    response = requests.post(url, data=data)
    json_response = response.json()

    if 'approval_request' in json_response:
        user.profile.authy_status = 'onetouch'
    else:
        user.profile.authy_status = 'sms'

    user.profile.save()
    return json_response


def send_authy_token_request(authy_user_id):
    authy_client = get_authy_client()

    authy_client.users.request_sms(authy_user_id)


def verify_authy_token(authy_user_id, token):
    authy_client = get_authy_client()

    return authy_client.tokens.verify(authy_user_id, token)


def check_user_status(user):
    authy_client = get_authy_client()
    return authy_client.users.status(user.profile.authy_id)