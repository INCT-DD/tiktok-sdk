"""Request and response models for the TikTok Shop Research API."""

from enum import StrEnum

from pydantic import BaseModel, Field, field_validator

from TikTok.ValidationModels.BaseModels import BaseRequestModel, ResponseErrorModel


class ShopInfoQueryFields(StrEnum):
    """Fields for a shop that operates in the EU."""

    shop_id = "shop_id"
    shop_name = "shop_name"
    shop_rating = "shop_rating"
    shop_review_count = "shop_review_count"
    item_sold_count = "item_sold_count"
    shop_performance_value = "shop_performance_value"


class ShopProductQueryFields(StrEnum):
    """Fields for a product available for purchase in the EU."""

    product_id = "product_id"
    product_name = "product_name"
    product_description = "product_description"
    product_price = "product_price"
    product_sold_count = "product_sold_count"
    product_review_count = "product_review_count"
    product_rating_1_count = "product_rating_1_count"
    product_rating_2_count = "product_rating_2_count"
    product_rating_3_count = "product_rating_3_count"
    product_rating_4_count = "product_rating_4_count"
    product_rating_5_count = "product_rating_5_count"
    shop_name = "shop_name"


class ShopReviewQueryFields(StrEnum):
    """Fields for a review of a product available for purchase in the EU."""

    product_name = "product_name"
    review_text = "review_text"
    review_like_count = "review_like_count"
    create_time = "create_time"
    review_rating = "review_rating"


class _ShopRequestModel(BaseRequestModel):
    """Send the selected fields as a comma-separated string in the request body."""

    fields: str = Field(min_length=1)


class ShopInfoRequestModel(_ShopRequestModel):
    """Find shops by name. Request between one and ten results."""

    shop_name: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=10, strict=True)


class _ShopPageRequestModel(_ShopRequestModel):
    """Select a page by number. The first page is 1. A page holds up to ten items."""

    page_start: int = Field(default=1, ge=1, strict=True)
    page_size: int = Field(default=10, ge=1, le=10, strict=True)


class ShopProductsRequestModel(_ShopPageRequestModel):
    """Select one page of products by the numeric shop ID."""

    shop_id: int = Field(strict=True)

    @field_validator("shop_id", mode="before", json_schema_input_type=int | str)
    @classmethod
    def accept_text_shop_id(cls, value: object) -> object:
        """Convert a decimal shop ID in a string to its request integer.

        The request table shows a quoted shop ID. Let Pydantic reject any
        value that does not supply an integer or its decimal digits.
        """
        return int(value) if isinstance(value, str) and value.isdecimal() else value


class ShopReviewsRequestModel(_ShopPageRequestModel):
    """Select one page of reviews by the product ID. Send this ID as a string."""

    product_id: str = Field(min_length=1)

    @field_validator("product_id", mode="before", json_schema_input_type=str | int)
    @classmethod
    def accept_numeric_product_id(cls, value: object) -> object:
        """Convert an integer ID from a product result to its request string.

        Preserve string IDs, including leading zeros. Let Pydantic check each
        other input against the string field.
        """
        return str(value) if type(value) is int else value


class ShopInfoDataModel(BaseModel):
    """Selected shop fields. The API returns the shop rating as a string."""

    shop_id: int | None = None
    shop_name: str | None = None
    shop_rating: str | None = None
    shop_review_count: int | None = None
    item_sold_count: int | None = None
    shop_performance_value: int | None = None


class ShopProductDataModel(BaseModel):
    """Selected product fields, including a rating if TikTok supplies one.

    Each price string includes its currency. The API can reject product_rating
    as a request field, although its product schema defines this response field.
    """

    product_id: int | None = None
    product_name: str | None = None
    product_description: str | None = None
    product_price: list[str] | None = None
    product_sold_count: int | None = None
    product_review_count: int | None = None
    product_rating: str | None = None
    product_rating_1_count: int | None = None
    product_rating_2_count: int | None = None
    product_rating_3_count: int | None = None
    product_rating_4_count: int | None = None
    product_rating_5_count: int | None = None
    shop_name: str | None = None


class ShopReviewDataModel(BaseModel):
    """Selected review fields. Keep the integer timestamp that TikTok returns.

    The display name is available if TikTok includes it in a result.
    """

    product_name: str | None = None
    review_text: str | None = None
    review_like_count: int | None = None
    create_time: int | None = None
    review_rating: str | None = None
    display_name: str | None = None


class ShopInfoResponseDataModel(BaseModel):
    """Shops that match the requested name."""

    shop_data: list[ShopInfoDataModel]


class ShopProductsResponseDataModel(BaseModel):
    """Products on the requested page."""

    product_data: list[ShopProductDataModel]


class ShopReviewsResponseDataModel(BaseModel):
    """Reviews on the requested page."""

    review_data: list[ShopReviewDataModel]


class ShopInfoResponseModel(BaseModel):
    """Shop results and the error details, if TikTok includes them."""

    data: ShopInfoResponseDataModel
    error: ResponseErrorModel | None = None


class ShopProductsResponseModel(BaseModel):
    """Product results and the error details, if TikTok includes them."""

    data: ShopProductsResponseDataModel
    error: ResponseErrorModel | None = None


class ShopReviewsResponseModel(BaseModel):
    """Review results and the error details, if TikTok includes them."""

    data: ShopReviewsResponseDataModel
    error: ResponseErrorModel | None = None
