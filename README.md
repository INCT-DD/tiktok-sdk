# TikTok

[![DOI](https://zenodo.org/badge/852515176.svg)](https://doi.org/10.5281/zenodo.13968316)

TikTok is an asynchronous Python SDK for the public TikTok Research API. It requires Python 3.15 or later and an approved Research API project. It covers the 15 operations in the Research API reference, including Batch Compliance and Research Shop. [TikTok Research API](https://developers.tiktok.com/docs/en/research-api-specs-query-videos)

## Connect

Run the examples in an async function or a notebook. Set `CLIENT_KEY` and `CLIENT_SECRET` to the credentials for your research project. The SDK requests a client access token and uses it for Research API calls. [Research API access](https://developers.tiktok.com/docs/en/research-api-get-started)

```python
from os import environ

from TikTok.Auth import OAuth2
from TikTok.Query import Query
from TikTok.ValidationModels.OAuth2 import RequestHeadersModel, TokenRequestBodyModel

auth = await OAuth2.authenticate(
    headers=RequestHeadersModel(),
    body=TokenRequestBodyModel(
        client_key=environ["CLIENT_KEY"],
        client_secret=environ["CLIENT_SECRET"],
    ),
)
query = Query(auth)
```

## Available operations

| Query methods | Inputs and results |
| --- | --- |
| `video.search` | Supply a search request and the fields to return. Read `data.videos`. To continue, use both `data.cursor` and `data.search_id`. The final page can omit the cursor. |
| `video.comments` | Supply `video_id` for comments or `comment_id` for replies. Choose one ID and at least one field. Both modes return `data.comments` and support an index cursor. |
| `user.info` | Select profile fields such as `display_name` and `bio_url`. Read them from `response.data`. |
| `user.liked_videos`, `user.reposted_videos` | Select video fields for a username. Read `data.user_liked_videos` or `data.reposted_videos`. Pass the returned cursor unchanged when `has_more` is true. Reposts use an index cursor. |
| `user.pinned_videos` | Select video fields for a username. Read `data.pinned_videos_list` in a single response. |
| `user.followers`, `user.following` | Supply a username and an optional count or cursor. The cursor is a UTC Unix timestamp in seconds. Each account has a username and display name. |
| `playlist.info` | Supply a playlist ID. Use `cursor` and `max_count` to page through video IDs. Pass `fields` to request playlist metadata. TikTok can return additional fields. |
| `compliance.create`, `compliance.status`, `compliance.download` | Submit video or comment IDs, check the task status, and download the file of valid IDs. |
| `shop.info`, `shop.products`, `shop.reviews` | Look up EU shops by name, products by shop ID, and reviews by product ID. Shop fields are sent in the JSON body. |

Each data query returns a typed response with a `data` attribute. Compliance downloads return bytes. An unavailable video or comment can produce an empty comment page. TikTok request failures raise `TikTok.Exceptions.Query.QueryException`. Its `code`, `status_code`, and `log_id` properties carry the available error details. Invalid arguments raise `ValueError`. A successful JSON response that does not fit its model raises a Pydantic `ValidationError`.

## Search for videos

Use `VideoQueryFieldName` for filters and `VideoQueryFields` for the fields to return. For example, `video_length` filters by a category such as `SHORT`, while the result field `video_duration` gives a duration in seconds.

```python
from TikTok.ValidationModels.Video import (
    VideoLength,
    VideoQueryFieldName,
    VideoQueryFields,
    VideoQueryOperation,
    VideoQueryRequestBuilder,
)

request = (
    VideoQueryRequestBuilder()
    .start_date("20240801")
    .end_date("20240815")
    .and_(VideoQueryOperation.IN, VideoQueryFieldName.region_code, ["BR", "PT"])
    .or_(VideoQueryOperation.EQ, VideoQueryFieldName.keyword, ["futebol"])
    .or_(VideoQueryOperation.EQ, VideoQueryFieldName.hashtag_name, ["esporte"])
    .not_(VideoQueryOperation.EQ, VideoQueryFieldName.video_length, [VideoLength.SHORT])
    .max_count(100)
    .build()
)
fields = [VideoQueryFields.id, VideoQueryFields.video_duration]
page = await query.video.search(request, fields)
if page.data.has_more and page.data.cursor is not None:
    next_request = request.model_copy(
        update={"cursor": page.data.cursor, "search_id": page.data.search_id}
    )
    next_page = await query.video.search(next_request, fields)
```

- Supply at least one nonempty group. All `and` conditions must match. At least one `or` condition must match when the group is present. Every `not` condition must be false.
- Use `EQ` for one value and `IN` for one or more values. Use `GT`, `GTE`, `LT`, and `LTE` with a single value for `create_date`, `view_count`, or `comment_count`. The SDK sends each operand as a string and accepts integers for numeric filters.
- The other filter names are `username`, `region_code`, `video_id`, `hashtag_name`, `keyword`, `music_id`, `effect_id`, and `video_length`. TikTok uses approximate text matching. The four duration categories are `SHORT`, `MID`, `LONG`, and `EXTRA_LONG`.
- Use `VideoRegionCode` from `TikTok.ValidationModels.VideoHelper` to select a published region code.
- Give UTC calendar dates in `YYYYMMDD` format. The end date can be the start date or up to 30 days later. Use `is_random(True)` to request a random sample.
- Search, liked, pinned, and reposted videos expose hashtag, sticker, effect, mention, label, and tag metadata. TikTok's references disagree on the meanings of AI tag codes 1 and 2. The SDK preserves the names and values returned by each endpoint. [Query Videos](https://developers.tiktok.com/docs/en/research-api-specs-query-videos) · [Query guide](https://developers.tiktok.com/docs/en/research-api-get-started) · [Pinned Videos](https://developers.tiktok.com/docs/en/research-api-specs-query-user-pinned-videos)

## Read comments and replies

```python
from TikTok.ValidationModels.Video import VideoCommentFields

fields = [VideoCommentFields.id, VideoCommentFields.display_name]
comments = await query.video.comments(video_id=video_id, fields=fields)
replies = await query.video.comments(comment_id=comment_id, fields=fields)
```

Use IDs from a video search or a comments response. Both calls accept `cursor` and `max_count`. TikTok defaults to 10 comments and allows up to 100. [Video Comments](https://developers.tiktok.com/docs/en/research-api-specs-query-video-comments)

The user profile selector supports `bio_url`. TikTok can also return `username` and an author profile URL as response data. Requests that select either profile URL spelling or `username` currently return an API error. [User Info](https://developers.tiktok.com/docs/en/research-api-specs-query-user-info) · [TikTok changelog](https://developers.tiktok.com/docs/en/changelog)

## Check a batch of IDs

```python
from pathlib import Path

from TikTok.ValidationModels.Compliance import ComplianceCategory, ComplianceTaskStatus

task = await query.compliance.create(ComplianceCategory.video, [video_id])
status = await query.compliance.status(task.data.task_id)
if status.data.task_status == ComplianceTaskStatus.completed:
    valid_ids = await query.compliance.download(task.data.task_id)
    Path("valid-video-ids.txt").write_bytes(valid_ids)
```

Supply one to 10,000 IDs of one category, either `video` or `comment`. You can also pass the path to a UTF-8 ID file. The SDK uploads a multipart text file. Check the same task ID again if the status is `Processing`. A `Failed` task has no completed result. [Batch Compliance](https://developers.tiktok.com/docs/en/batch-compliance-apis)

## Query Research Shop

```python
from TikTok.ValidationModels.Shop import (
    ShopInfoQueryFields,
    ShopProductQueryFields,
    ShopReviewQueryFields,
)

shops = await query.shop.info("Test Shop", [ShopInfoQueryFields.shop_id], limit=1)
if shops.data.shop_data:
    products = await query.shop.products(
        shops.data.shop_data[0].shop_id, [ShopProductQueryFields.product_id], page_size=1
    )
    if products.data.product_data:
        reviews = await query.shop.reviews(
            products.data.product_data[0].product_id,
            [ShopReviewQueryFields.review_rating],
            page_start=1,
            page_size=10,
        )
```

Each call requires at least one field. The shop lookup accepts a `limit` from 1 to 10. TikTok can return more matches than requested. Product and review pages start at 1 and hold up to 10 records. Select the next page with `page_start`. Prices keep their currency strings. The SDK preserves the review timestamp and rating as supplied by TikTok. [Shop Info](https://developers.tiktok.com/docs/en/research-api-specs-query-tiktok-shop-info) · [Shop Products](https://developers.tiktok.com/docs/en/research-api-specs-query-tiktok-shop-products) · [Shop Reviews](https://developers.tiktok.com/docs/en/research-api-specs-query-tiktok-shop-reviews)

The product and review models can read `product_rating` and review `display_name` if TikTok returns them. The service currently rejects these names as field selections.

## Migrate from version 3

- Read liked videos from `response.data.user_liked_videos`. The same object contains `cursor` and `has_more`.
- Replace output-only search filters with supported filter names. Use `keyword` to search descriptions. The older Python enum members `id`, `create_time`, `effect_ids`, and `video_duration` now send `video_id`, `create_date`, `effect_id`, and `video_length`. Direct JSON requests require the wire names.
- Keep using `favorites_count` for result selection on all four video routes. Search results expose their identifier through `video.id` for either spelling returned by TikTok.
- A TikTok error can arrive with HTTP 200. Catch `QueryException` to handle service errors. When you finish using the SDK, close both HTTP clients with `await query.client.aclose()` and `await auth.client.aclose()`.

# Citation

If you use this library in your work, please cite it as follows:

```
@misc{teles_tiktok_sdk_2024,
  author       = {Alexandre Teles},
  title        = {{TikTok Research API SDK}},
  year         = 2024,
  doi          = {10.5281/zenodo.13968316},
  url          = {https://github.com/INCT-DD/tiktok-sdk},
  institution  = {Instituto Nacional de Ciência e Tecnologia em Democracia Digital},
}
```
