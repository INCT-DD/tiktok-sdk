"""
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
from TikTok.ValidationModels.OAuth2 import RequestHeadersModel, TokenRequestBodyModel

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
from TikTok.ValidationModels.User import UserInfoQueryFields

query = Query(auth)

    user_info = await query.user.info(
        username="example_username",
        fields=[
            UserInfoQueryFields.display_name,
            UserInfoQueryFields.follower_count,
            UserInfoQueryFields.following_count,
            UserInfoQueryFields.video_count,
            UserInfoQueryFields.likes_count,
        ],
    )

print(user_info)
```

Given the complexity of video queries, this library provides a helper class to build them.
It introduces some level of indirection and API inconsistency, but its introduction was a deliberate design choice to help users create queries
that are easy to understand and modify without the need to manually write the JSON object or learn a dedicated DSL.

```python
# Example: Build a query to search for videos uploaded by "example_username" between August 1st and August 2nd, 2024.
from TikTok.Query import Query
from TikTok.ValidationModels.Video import (
    VideoQueryRequestBuilder,
    VideoQueryOperation,
    VideoQueryFieldName,
    VideoRegionCode,
    VideoQueryFields,
)

query = Query(auth)

video_query = VideoQueryRequestBuilder()

request = (
    video_query.start_date("20240801")
    .end_date("20240802")
    .max_count(100)
    .and_(VideoQueryOperation.EQ, VideoQueryFieldName.username, ["example_username"])
    .build()
)

video_query_response = await query.video.search(
    request=request, fields=[VideoQueryFields.id, VideoQueryFields.voice_to_text]
)

```

If you are interested in learning more about the underlying API, you can find the documentation here: [https://developers.tiktok.com/doc/research-api-specs-query-videos](https://developers.tiktok.com/doc/research-api-specs-query-videos)

"""
