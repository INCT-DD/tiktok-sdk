# TikTok

TikTok is a Python library for interacting with the TikTok Research API.

This library provides a simple and efficient way to access TikTok's API endpoints,
allowing developers to retrieve user information, video details, and other data.

TikTok is built on top of the `httpx` library, which is a powerful and flexible HTTP library,
and uses `orjson` for efficient JSON serialization and deserialization.

This library is designed to be easy to use and understand,
with a focus on providing a simple and intuitive interface for accessing TikTok's API
while being fully asynchronous, typed and compatible with the latest Python standards.

To get started, assuming you have access to the TikTok Research API, create a new instance
of the Auth class with your API key and secret:

```python
from TikTok.Auth import OAuth2
from TikTok.Types.OAuth2 import RequestHeadersModel, TokenRequestBodyModel

auth: OAuth2 = await OAuth2.authenticate(
    headers=RequestHeadersModel(),
    body=TokenRequestBodyModel(
        client_key="YOUR_CLIENT_KEY",
        client_secret="YOUR_CLIENT_SECRET",
    ),
)
```

Once you have an instance of the Auth class, you can use it to authenticate your queries to the TikTok API.
For example, to retrieve information about a user, you can use the following code:

```python
from TikTok.Query import Query
from TikTok.Types.User import QueryFields as UserQueryFields

query = Query(auth)

user_info = await query.user(
    username="USERNAME",
    fields=[
        UserQueryFields.display_name,
        UserQueryFields.biography,
        UserQueryFields.id,
    ],
)

print(user_info)
```
