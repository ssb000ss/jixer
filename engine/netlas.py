from urllib.parse import urljoin

import grequests

from engine.base import BaseApiClient


class NetlasClient(BaseApiClient):
    """
    Client for working with the Netlas API.

    Attributes:
        BASE_URL (str): Base URL for Netlas API requests.
        COUNT_ENDPOINT (str): Endpoint for counting items.
        SEARCH_ENDPOINT (str): Endpoint for search queries.
        HEADERS (dict): Headers for API requests.
        PARAMS (dict): API request parameters.
        _IP_KWORD (str): Key for extracting IP addresses from results.
        _COUNT_KWORD (str): Key to retrieve the count in the API response.
        _QUERY_KWORD (str): Key to pass the search query.
        _RESULTS_PER_PAGE (int): Number of results per page.
        _TOTAL_ITEMS_KWORD (str): Key to retrieve the total number of items in the API response.
    """

    def __init__(self, api_key):
        """
        Initializes the NetlasClient object.

        Args:
            api_key (str): Client's API key.
        """
        super().__init__(api_key)
        self.BASE_URL = 'https://app.netlas.io/api/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'responses_count')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'responses')
        self.HEADERS['X-API-Key'] = self.api_key
        self.PARAMS = {
            'source_type': 'include',
            'fields': 'ip',
        }
        self._IP_KWORD = 'ip'
        self._COUNT_KWORD = 'count'
        self._PAGE_KWORD = 'start'
        self._QUERY_KWORD = 'q'
        self._RESULTS_PER_PAGE = 20
        self._TOTAL_ITEMS_KWORD = 'items'

    def get_request_page_list(self, query: str, count: int):
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
            pages = self.get_page_count(count)
            params = self.PARAMS.copy()
            params[self._QUERY_KWORD] = query
            for page in range(pages):
                params = params.copy()
                params.update({self._PAGE_KWORD: page * self._RESULTS_PER_PAGE})
                request_list.append(grequests.get(self.SEARCH_ENDPOINT, params=params, headers=self.HEADERS))
        return request_list

    def get_parsed_ip_list(self, results) -> set:
        """
        Extract IP addresses from the query results.

        Args:
            results: Query results.

        Returns:
            set[str]: Set of IP addresses.
        """
        return set([_.get('data').get('ip') for _ in results])

    def __str__(self):
        return 'netlas'
