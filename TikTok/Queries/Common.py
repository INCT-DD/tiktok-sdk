"""
This module contains the QueryClass, which serves as a base class for handling common API queries.

The QueryClass is designed to encapsulate shared functionality and attributes for subclasses that interact 
with the TikTok API. It provides a reference to the parent Query instance, allowing subclasses to access 
authentication and endpoint information.

Usage:
    Subclasses can inherit from QueryClass to implement specific API query methods, ensuring 
    consistent handling of API requests and responses.
"""

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
