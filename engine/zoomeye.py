from urllib.parse import urljoin
import grequests
from engine.base import BaseApiClient


class ZoomeyeClient(BaseApiClient):
    """
    Client for working with the ZoomEye API.

    Attributes:
        BASE_URL (str): Base URL for ZoomEye API requests.
        COUNT_ENDPOINT (str): Endpoint for counting items.
        SEARCH_ENDPOINT (str): Endpoint for search queries.
        HEADERS (dict): Headers for API requests.
        PARAMS (dict): API request parameters.
        _QUERY_KWORD (str): Key to pass the search query.
        _COUNT_KWORD (str): Key to retrieve the count in the API response.
        _IP_KWORD (str): Key to retrieve IP addresses from the API response.
        _RESULTS_PER_PAGE (int): Maximum number of results per page.
        _TOTAL_ITEMS_KWORD (str): Key to retrieve the total number of items in the API response.
    """

    def __init__(self, api_key: str):
        """
        Initializes the ZoomeyeClient object.

        Args:
            api_key (str): ZoomEye client's API key.
        """
        super().__init__(api_key)
        self.BASE_URL = 'https://api.zoomeye.org/host/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'search')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'search')
        self.HEADERS['API-KEY'] = self.api_key
        self._IP_KWORD = 'ip'
        self._COUNT_KWORD = 'total'
        self._QUERY_KWORD = 'query'
        self._RESULTS_PER_PAGE = 20
        self._TOTAL_ITEMS_KWORD = 'matches'

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
            params['query'] = query
            for page in range(1, pages + 1):
                params = params.copy()
                params.update({self._PAGE_KWORD: page})
                request_list.append(grequests.get(self.SEARCH_ENDPOINT, params=params, headers=self.HEADERS))
        return request_list

    def get_parsed_ip_list(self, results: list) -> set:
        """
        Extract IP addresses from the query results.

        Args:
            results (list): Query results.

        Returns:
            set[str]: Set of IP addresses.
        """
        return set([_.get('ip') for _ in results])

    def __str__(self) -> str:
        return 'zoomeye'
