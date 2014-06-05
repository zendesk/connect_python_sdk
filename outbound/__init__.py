import sys
import json
from numbers import Number

import requests

import version

__BASE_URL = "http://api.ob-dev.com:9001"

this = sys.modules[__name__]

class NoApiKeyException(Exception):
    pass

class InvalidUserIdException(Exception):
    pass

class InvalidEventException(Exception):
    pass

def init(key):
    setattr(this, '__HEADERS', {
        'content-type': 'application/json',
        'X-Outbound-Client': 'python',
        'X-Outbound-Client-Version': version.VERSION,
        'X-Outbound-Key': key,})

def identify(user_id, first_name=None, last_name=None, email=None,
            phone_number=None, apns_tokens=None, gcm_tokens=None, attributes=None):
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
    """

    if not hasattr(this, '__HEADERS'):
        raise NoApiKeyException()

    if not isinstance(user_id, (basestring, Number)):
        raise InvalidUserIdException()

    data = __user(
        first_name,
        last_name,
        email,
        phone_number,
        apns_tokens,
        gcm_tokens,
        attributes,)
    data['user_id'] = user_id

    requests.post(
        "%s/identify" % __BASE_URL,
        data=json.dumps(data),
        headers=getattr(this, '__HEADERS'),)

def track(user_id, event, first_name=None, last_name=None, email=None,
        phone_number=None, apns_tokens=None, gcm_tokens=None,
        user_attributes=None, payload=None):
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

    :param dict payload: An optional dictionary with any attributes that
    describe the event being track. Example: if the event were "added item to
    cart", you might include a payload attribute named "item" that is the name
    of the item added to the cart.
    """

    if not hasattr(this, '__HEADERS'):
        raise NoApiKeyException('No API key detected. Call init() before calling track().')

    if not isinstance(user_id, (basestring, Number)):
        raise InvalidUserIdException()
    if not isinstance(event, basestring):
        raise InvalidEventException()

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

    if payload:
        if isinstance(payload, dict):
            if len(payload) > 0:
                data['payload'] = payload
        else:
            sys.stderr.write('Invalid event payload given. Expected dictionary. ' +
                        'Got %s' % type(payload).__name__)

    requests.post(
        "%s/track" % __BASE_URL,
        data=json.dumps(data),
        headers=getattr(this, '__HEADERS'),)

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
