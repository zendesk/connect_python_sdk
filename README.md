# Outbound Python Library

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
        payload=dict(
            eventAttr="",
        ),
        attributes=dict(
            some_custom_attriute="Loren Ipsum",
        ),
        on_error=on_error_callback_function,
        on_success=on_success_callback_func,
    )
