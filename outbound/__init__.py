import sys
import json
from numbers import Number

import requests

import version

__BASE_URL = "https://api.outbound.io/v2"

this = sys.modules[__name__]

ERROR_INIT = 1
ERROR_USER_ID = 2
ERROR_EVENT_NAME = 3
ERROR_CONNECTION = 4
ERROR_UNKNOWN = 5
ERROR_TOKEN = 6

APNS = "apns"
GCM = "gcm"

def init(key):
    setattr(this, '__HEADERS', {
        'content-type': 'application/json',
        'X-Outbound-Client': 'Python/{0}'.format(version.VERSION),
        'X-Outbound-Key': key,})

def disable_token(platform, user_id, token, on_error=None, on_success=None):
    """ Disable a device token for a user.

    :param str platform The platform which to disable token on. One of either
    Google Cloud Messaging (outbound.GCM) or Apple Push Notification Service
    (outbound.APNS).

    :param str | number user_id: the id you use to identify a user. this should
    be static for the lifetime of a user.

    :param str token: the token to disable.

    :param func on_error: An optional function to call in the event of an error.
    on_error callback should take 2 parameters: `code` and `error`. `code` will be
    one of outbound.ERROR_XXXXXX. `error` will be the corresponding message.

    :param func on_success: An optional function to call if/when the API call succeeds.
    on_success callback takes no parameters.
    """
    __device_token(platform, False, user_id, token, on_error, on_success)

def register_token(platform, user_id, token, on_error=None, on_success=None):
    """ Register a device token for a user.

    :param str platform The platform which to register token on. One of either
    Google Cloud Messaging (outbound.GCM) or Apple Push Notification Service
    (outbound.APNS).

    :param str | number user_id: the id you use to identify a user. this should
    be static for the lifetime of a user.

    :param str token: the token to register.

    :param func on_error: An optional function to call in the event of an error.
    on_error callback should take 2 parameters: `code` and `error`. `code` will be
    one of outbound.ERROR_XXXXXX. `error` will be the corresponding message.

    :param func on_success: An optional function to call if/when the API call succeeds.
    on_success callback takes no parameters.
    """
    __device_token(platform, True, user_id, token, on_error, on_success)

def identify(user_id, first_name=None, last_name=None, email=None,
            phone_number=None, apns_tokens=None, gcm_tokens=None,
            attributes=None, on_error=None, on_success=None):
    """ Identifying a user creates a record of your user in Outbound. Identify
    calls should be made prior to sending any events for a user.

    :param str | number user_id: the id you use to identify a user. this should
    be static for the lifetime of a user.

    :param str first_name: OPTIONAL the user's first name.

    :param str last_name: OPTIONAL the user's last name.

    :param str email: OPTIONAL the user's email address.

    :param str phone_number: OPTIONAL the user's phone number.

    :param str | list apns_tokens: OPTIONAL the device tokens for the user's iOS
    devices. If a single string is given it is put into a list.

    :param str | list gcm_tokens: OPTIONAL the device tokens for the user's Android
    devices. If a single string is given it is put into a list.

    :param dict attributes: An optional dictionary with any additional freeform
    attributes describing the user.

    :param func on_error: An optional function to call in the event of an error.
    on_error callback should take 2 parameters: `code` and `error`. `code` will be
    one of outbound.ERROR_XXXXXX. `error` will be the corresponding message.

    :param func on_success: An optional function to call if/when the API call succeeds.
    on_success callback takes no parameters.
    """

    on_error = on_error or __on_error
    on_success = on_success or __on_success

    if not hasattr(this, '__HEADERS'):
        on_error(ERROR_INIT, __error_message(ERROR_INIT))
        return

    if not isinstance(user_id, (basestring, Number)):
        on_error(ERROR_USER_ID, __error_message(ERROR_USER_ID))
        return

    data = __user(
        first_name,
        last_name,
        email,
        phone_number,
        apns_tokens,
        gcm_tokens,
        attributes,)
    data['user_id'] = user_id

    try:
        resp = requests.post(
            "%s/identify" % __BASE_URL,
            data=json.dumps(data),
            headers=getattr(this, '__HEADERS'),)

        if resp.status_code >= 200 and resp.status_code < 400:
            on_success()
        else:
            on_error(ERROR_UNKNOWN, resp.text)
    except requests.exceptions.ConnectionError:
        on_error(ERROR_CONNECTION, __error_message(ERROR_CONNECTION))

def track(user_id, event, first_name=None, last_name=None, email=None,
        phone_number=None, apns_tokens=None, gcm_tokens=None,
        user_attributes=None, properties=None, on_error=None, on_success=None):
    """ For any event you want to track, when a user triggers that event you
    would call this function.

    You can do an identify and track call simultaneously by including all the
    identifiable user information in the track call.

    :param str | number user_id: the id you user who triggered the event.

    :param str first_name: OPTIONAL the user's first name.

    :param str last_name: OPTIONAL the user's last name.

    :param str email: OPTIONAL the user's email address.

    :param str phone_number: OPTIONAL the user's phone number.

    :param str | list apns_tokens: OPTIONAL the device tokens for the user's iOS
    devices. If a single string is given it is put into a list.

    :param str | list gcm_tokens: OPTIONAL the device tokens for the user's Android
    devices. If a single string is given it is put into a list.

    :param dict user_attributes: An optional dictionary with any additional
    freeform attributes describing the user.

    :param dict properties: An optional dictionary with any properties that
    describe the event being track. Example: if the event were "added item to
    cart", you might include a properties named "item" that is the name
    of the item added to the cart.

    :param func on_error: An optional function to call in the event of an error.
    on_error callback should take 1 parameter which will be the error message.

    :param func on_success: An optional function to call if/when the API call succeeds.
    on_success callback takes no parameters.
    """

    on_error = on_error or __on_error
    on_success = on_success or __on_success

    if not hasattr(this, '__HEADERS'):
        on_error(ERROR_INIT, __error_message(ERROR_INIT))
        return

    if not isinstance(user_id, (basestring, Number)):
        on_error(ERROR_USER_ID, __error_message(ERROR_USER_ID))
        return
    if not isinstance(event, basestring):
        on_error(ERROR_EVENT_NAME, __error_message(ERROR_EVENT_NAME))
        return

    data = dict(user_id=user_id, event=event)
    user = __user(
        first_name,
        last_name,
        email,
        phone_number,
        apns_tokens,
        gcm_tokens,
        user_attributes,)
    if user:
        data['user'] = user

    if properties:
        if isinstance(properties, dict):
            if len(properties) > 0:
                data['properties'] = properties
        else:
            sys.stderr.write('Invalid event properties given. Expected dictionary. ' +
                        'Got %s' % type(properties).__name__)

    try:
        resp = requests.post(
            "%s/track" % __BASE_URL,
            data=json.dumps(data),
            headers=getattr(this, '__HEADERS'),)

        if resp.status_code >= 200 and resp.status_code < 400:
            on_success()
        else:
            on_error(ERROR_UNKNOWN, resp.text)
    except requests.exceptions.ConnectionError:
        on_error(ERROR_CONNECTION, __error_message(ERROR_CONNECTION))

def __device_token(platform, register, user_id, token, on_error=None, on_success=None):
    on_error = on_error or __on_error
    on_success = on_success or __on_success

    if not hasattr(this, '__HEADERS'):
        on_error(ERROR_INIT, __error_message(ERROR_INIT))
        return

    if not isinstance(user_id, (basestring, Number)):
        on_error(ERROR_USER_ID, __error_message(ERROR_USER_ID))
        return

    if not isinstance(token, basestring):
        on_error(ERROR_TOKEN, __error_message(ERROR_TOKEN))
        return

    try:
        resp = requests.post(
            "%s/%s/%s" % __BASE_URL, platform, 'register' if register else 'disable',
            data=json.dumps(dict(
                user_id=user_id,
                token=token,
            )),
            headers=getattr(this, '__HEADERS'),)

        if resp.status_code >= 200 and resp.status_code < 400:
            on_success()
        else:
            on_error(ERROR_UNKNOWN, resp.text)
    except requests.exceptions.ConnectionError:
        on_error(ERROR_CONNECTION, __error_message(ERROR_CONNECTION))

def __user(first_name, last_name, email, phone_number, apns_tokens,
        gcm_tokens, attributes):

    data = dict()
    if first_name:
        data['first_name'] = first_name
    if last_name:
        data['last_name'] = last_name
    if email:
        data['email'] = email
    if phone_number:
        data['phone_number'] = phone_number
    if apns_tokens:
        if isinstance(apns_tokens, basestring):
            apns_tokens = [apns_tokens]
        if isinstance(apns_tokens, (list, tuple)):
            data['apns'] = apns_tokens
        else:
            sys.stderr.write('Invalid APNS tokens given. Expected string or ' +
                        'list of strings. Got %s' % type(apns_tokens).__name__)
    if gcm_tokens:
        if isinstance(gcm_tokens, basestring):
            gcm_tokens = [gcm_tokens]
        if isinstance(gcm_tokens, (list, tuple)):
            data['gcm'] = gcm_tokens
        else:
            sys.stderr.write('Invalid GCM tokens given. Expected string or ' +
                        'list of strings. Got %s' % type(gcm_tokens).__name__)

    if attributes:
        if isinstance(attributes, dict):
            if len(attributes) > 0:
                data['attributes'] = attributes
        else:
            sys.stderr.write('Invalid user attributes given. Expected dictionary. ' +
                        'Got %s' % type(attributes).__name__)

    return data

def __error_message(code):
    if code == ERROR_INIT:
        return "init() must be called before identifying any users."
    elif code == ERROR_USER_ID:
        return "User ID must be a string or a number."
    elif code == ERROR_EVENT_NAME:
        return "Event name must be a string."
    elif code == ERROR_CONNECTION:
        return "Unable to connect to Outbound."
    elif code == ERROR_UNKNOWN:
        return "Unknown error occurred."
    elif code == ERROR_TOKEN:
        return "Token must be a string."

def __on_error(code, err):
    pass

def __on_success():
    pass
