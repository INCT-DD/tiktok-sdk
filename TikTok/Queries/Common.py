from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TikTok.Query import Query


class QueryClass:
    """
    A subclass to handle common API queries.

    Attributes:
        query (Query): The parent Query instance.
    """

    def __init__(self, query: "Query") -> None:
        """
        Initializes the QueryClass subclass with a reference to the parent Query instance.

        Parameters:
            query (Query): The parent Query instance.
        """
        self.query = query
