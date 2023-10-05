from urllib.parse import urljoin

import grequests

from engine.base import BaseApiClient
from utils.helper import query_to_bs64


class FofaClient(BaseApiClient):
    """
    Client for working with the Fofa API.

    Attributes:
        BASE_URL (str): Base URL for Fofa API requests.
        COUNT_ENDPOINT (str): Endpoint for counting items.
        SEARCH_ENDPOINT (str): Endpoint for search queries.
        _COUNT_KWORD (str): Key to retrieve the count in the API response.
        _QUERY_KWORD (str): Key to pass the search query in Base64 encoding.
        _RESULTS_PER_PAGE (int): Number of results per page.
        _TOTAL_ITEMS_KWORD (str): Key to retrieve the total number of items in the API response.
        PARAMS (dict): API request parameters.
    """

    def __init__(self, api_key: str, email: str):
        """
        Initializes the FofaClient object.

        Args:
            api_key (str): Client's API key.
            email (str): Client's email address.
        """
        super().__init__(api_key)
        self.BASE_URL = 'https://fofa.info/api/v1/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'search/all')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'search/all')
        self._COUNT_KWORD = 'size'
        self._QUERY_KWORD = 'qbase64'
        self._RESULTS_PER_PAGE = 1000
        self._TOTAL_ITEMS_KWORD = 'results'
        self.PARAMS = {
            'email': email,
            'key': self.api_key,
            'size': self._RESULTS_PER_PAGE
        }

    def get_parsed_ip_list(self, results: list) -> list:
        """
        Extracts IP addresses from the query results.

        Args:
            results: Query results.

        Returns:
            set[str]: Set of IP addresses.
        """
        return set([_[1] for _ in results])

    def count(self, query: str) -> int:
        """
        Get the number of items matching the query.

        Args:
            query (str): Search query.

        Returns:
            int: Number of items matching the query.
        """
        query_b64 = query_to_bs64(query)
        return super().count(query_b64)

    def get_request_page_list(self, query: str, count: int) -> list:
        """
        Get a list of requests for paging the results.

        Args:
            query (str): Search query.
            count (int): Number of items matching the query.

        Returns:
            list[grequests.Request]: List of requests for searching by pages.
        """
        request_list = []
        if count > 0:
            pages = min(self.get_page_count(count), 2500)
            params = self.PARAMS.copy()
            params[self._QUERY_KWORD] = query_to_bs64(query)
            for page in range(1, pages + 1):
                params = params.copy()
                params.update({self._PAGE_KWORD: page})
                request_list.append(grequests.get(self.SEARCH_ENDPOINT, params=params, headers=self.HEADERS))
        return request_list

    def __str__(self):
        return 'fofa'
