# Outbound Python Library

## Installation

    pip install outbound

## Setup

    import outbound
    outbound.init("YOUR_API_KEY")

## Identify User

    import outbound
    outbound.identify(
        "USER_ID",
        first_name="First Name",
        last_name="Last Name",
        email="user@domain.com",
        phone_number="5551234567",
        apns_tokens=["ios device token"],
        gcm_tokens=["android device token"],
        attributes=dict(
            some_custom_attriute="Loren Ipsum",
        ),
        on_error=on_error_callback_function,
        on_success=on_success_callback_func,
    )

## Track Event

    import outbound
    outbound.track(
        "USER_ID",
        "EVENT NAME",
        properties=dict(
            eventAttr="",
        ),
        on_error=on_error_callback_function,
        on_success=on_success_callback_func,
    )

## Register/Revoke Device Token
If you have a mobile app and send push notifications to need to send your user's device tokens to Outbound. You can do that by including them in the `identify` call as shown above or by explicitly registering the tokens. You can also revoke a token if you no longer want to send notifications to that users. The first parameter of each of these function is the platform for which the token belongs. There are only 2 valid values which are `outbound.APNS` (Apple Push Notification Service - iOS) and `outbound.GCM` (Google Cloud Messaging - Android).

    import outbound
    outbound.register_token(
        outbound.APNS,
        "USER_ID",
        "TOKEN"
        on_error=on_error_callback_function,
        on_success=on_success_callback_func,
    )

    outbound.revoke_token(
        outbound.APNS,
        "USER_ID",
        "TOKEN"
        on_error=on_error_callback_function,
        on_success=on_success_callback_func,
    )

## Specifics
### User ID
- A user ID must ALWAYS be a string or a number. Anything else will trigger an error and the call will not be sent to Outbound. User IDs are always stored as strings. Keep this in mind if you have different types. A user with ID of 1 (the number) will be considered the same as user with ID of "1" (the string).
- A user ID should be static. It should be the same value you use to identify the user in your own system.

### Event Name
- An event name in a track can only be a string. Any other type of value will trigger an error and the call will not be sent to Outbound.
- Event names can be anything you want them to be (as long as they are strings) and contain any character you want.

### Device Tokens
- If you send a device token through an `identify` call, that is equivalent to sending a `register` call. Regardless of the state of that token it will become active again and we will attempt to send notifications to it. It is recommended that if you use the `register` and `revoke` calls that you DO NOT send any tokens in `identify` calls. This way you can more easily control the state of your tokens.

### Callbacks
- `on_error` callback takes a two parameters. The first is an integer code corresponding to one of `outbound.ERROR_XXXXX`. The second is a string. Will either be a stock string describing the error or in the case of an error reponse from Outbound it will be the body of the response.
- `on_success` callback takes no parameters.
