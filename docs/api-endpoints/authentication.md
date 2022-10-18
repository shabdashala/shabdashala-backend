Login and Authentication API endpoints
==============================

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
