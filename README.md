API endpoints
=============

Registration
------------

- /api/auth/registration/ (POST)
    - first_name
    - last_name
    - email
    - password
    - password_confirmation

- /api/auth/registration/verify-email/ (POST)
    - key


Login and Authentication
-------------------------
- /api/auth/login/ (POST)
    - email
    - password

    Returns
    ```json
    {
        "key": "b0c77e5c54a8cd3bc8103eb571114f0a979650db",
        "user": {
            "id": 6,
            "email": "balu@shabdashala.com",
            "first_name": "Balu",
            "last_name": "Varanasi"
        }
    }
    ```


- /api/auth/logout/ (GET)
- /api/auth/password/reset/ (POST)
    - email

- /api/auth/password/reset/confirm/ (POST)
    - uid
    - token
    - new_password1
    - new_password2

    .. note:: uid and token are sent in email after calling /api/auth/password/reset/

- /api/auth/password/change/ (POST)

    - new_password1
    - new_password2
    - old_password

- /api/auth/user/ (GET, PUT, PATCH)

    - username
    - first_name
    - last_name

    Returns id, username, email, first_name, last_name

Accounts
--------

All these APIs are authorized by Token authentication. set the header `Authorization` to `Token <enter-the-token-you-received-after-login>`

    - READ - `/api/accounts/` - RETURNS USER DATA in a list.
    - READ SPECIFIC - `/api/accounts/[id]/` - GET
    - UPDATE SPECIFIC - `/api/accounts/[id]/` - PUT

- /api/accounts/ (GET)
    Returns
    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 6,
                "email": "bala@shabdashala.com",
                "mobile": "",
                "first_name": "Bala Subrahmanyam",
                "last_name": "Varanasi",
                "image": "",
                "gender": null
            }
        ]
    }
    ```

- /api/accounts/[id]/ (GET)
    Returns
    ```json
    {
        "id": 6,
        "email": "bala@shabdashala.com",
        "mobile": "",
        "first_name": "Bala Subrahmanyam",
        "last_name": "Varanasi",
        "profile_image": "https://shabdashala.s3.amazonaws.com/media/accounts/user/ca5ecf17-9bf9-42cb-8fde-2aa2c6a5a93d.jpg",
        "gender": null
    }
    ```

- /api/accounts/[id]/ (PUT)
    Returns
    - PUT keys
        - `first_name` (required)
        - `last_name` (required)
        - `gender` (required)
        - `profile_image` (required)


    Failed Response
    ```json
    {
        "first_name": [
            "This field is required."
        ],
        "last_name": [
            "This field is required."
        ],
        "gender": [
            "This field is required."
        ],
        "profile_image": [
            "This field is required."
        ]
    }
    ```

    Success Response
    ```json
    {
        "id": 6,
        "email": "bala@shabdashala.com",
        "mobile": "",
        "first_name": "Bala Subrahmanyam",
        "last_name": "Varanasi",
        "profile_image": "https://shabdashala.s3.amazonaws.com/media/accounts/user/ca5ecf17-9bf9-42cb-8fde-2aa2c6a5a93d.jpg",
        "gender": null
    }
    ``
