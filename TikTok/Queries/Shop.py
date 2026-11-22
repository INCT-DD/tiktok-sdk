"""Queries for public EU shop data in the TikTok Research API."""

from TikTok.Queries.Common import QueryClass
from TikTok.ValidationModels import Shop


class ShopQueries(QueryClass):
    """Look up a shop, its products, and the reviews for a product."""

    async def info(
        self,
        shop_name: str,
        fields: list[Shop.ShopInfoQueryFields],
        limit: int = 10,
    ) -> Shop.ShopInfoResponseModel:
        """Get shops that match a shop name.

        Supply the shop name and at least one field. Set limit to an integer
        from 1 to 10. TikTok can return more matches than requested. Read all
        returned shops from data.shop_data. Select shop_id for a products query.

        Invalid arguments raise ValueError. A failed API request raises
        QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.ShopInfoURL,
            response_model_class=Shop.ShopInfoResponseModel,
            request=Shop.ShopInfoRequestModel(
                shop_name=shop_name,
                limit=limit,
                fields=self._build_params(fields, Shop.ShopInfoQueryFields)["fields"],
            ),
        )

    async def products(
        self,
        shop_id: int | str,
        fields: list[Shop.ShopProductQueryFields],
        page_start: int = 1,
        page_size: int = 10,
    ) -> Shop.ShopProductsResponseModel:
        """Get one page of products that a shop offers in the EU.

        Supply the numeric shop ID and at least one field. The method also
        accepts an ID as a string of decimal digits. Pages start at 1.
        Set page_size to an integer from 1 to 10. Read the products from
        data.product_data. Select product_id to use a result in a reviews query.

        Invalid arguments raise ValueError. A failed API request raises
        QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.ShopProductsURL,
            response_model_class=Shop.ShopProductsResponseModel,
            request=Shop.ShopProductsRequestModel.model_validate(
                {
                    "shop_id": shop_id,
                    "page_start": page_start,
                    "page_size": page_size,
                    **self._build_params(fields, Shop.ShopProductQueryFields),
                }
            ),
        )

    async def reviews(
        self,
        product_id: str | int,
        fields: list[Shop.ShopReviewQueryFields],
        page_start: int = 1,
        page_size: int = 10,
    ) -> Shop.ShopReviewsResponseModel:
        """Get one page of reviews for a product available in the EU.

        Supply at least one field and a product ID as a string or an integer.
        The request sends the ID as a string. Pages start at 1. Set page_size
        to an integer from 1 to 10. Read the reviews from data.review_data.

        Invalid arguments raise ValueError. A failed API request raises
        QueryException.
        """
        return await self._fetch_data(
            url=self.query.endpoints.ShopReviewsURL,
            response_model_class=Shop.ShopReviewsResponseModel,
            request=Shop.ShopReviewsRequestModel.model_validate(
                {
                    "product_id": product_id,
                    "page_start": page_start,
                    "page_size": page_size,
                    **self._build_params(fields, Shop.ShopReviewQueryFields),
                }
            ),
        )
