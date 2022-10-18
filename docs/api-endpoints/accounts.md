Accounts API endpoints
======================

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
    ```
