from urllib.parse import urljoin
import grequests
from engine.base import BaseApiClient


class ShodanClient(BaseApiClient):
    """
    Client for working with the Shodan API.

    Attributes:
        BASE_URL (str): Base URL for Shodan API requests.
        COUNT_ENDPOINT (str): Endpoint for counting items.
        SEARCH_ENDPOINT (str): Endpoint for search queries.
        HEADERS (dict): Headers for API requests.
        PARAMS (dict): API request parameters.
        _QUERY_KWORD (str): Key to pass the search query.
        _COUNT_KWORD (str): Key to retrieve the count in the API response.
        _TOTAL_ITEMS_KWORD (str): Key to retrieve the total number of items in the API response.
    """

    def __init__(self, api_key: str):
        """
        Initializes the ShodanClient object.

        Args:
            api_key (str): Client's API key.
        """
        super().__init__(api_key)
        self.PARAMS['key'] = self.api_key
        self.BASE_URL = 'https://api.shodan.io/shodan/host/'
        self.COUNT_ENDPOINT = urljoin(self.BASE_URL, 'count')
        self.SEARCH_ENDPOINT = urljoin(self.BASE_URL, 'search')
        self._QUERY_KWORD = 'query'
        self._COUNT_KWORD = 'total'
        self._TOTAL_ITEMS_KWORD = 'matches'

    def get_parsed_ip_list(self, results: list) -> set:
        """
        Extracts IP addresses from the query results.

        Args:
            results (list): Query results.

        Returns:
            set[str]: Set of IP addresses.
        """
        return set([_.get('ip_str') for _ in results])

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
            pages = self.get_page_count(count)
            params = self.PARAMS.copy()
            params['query'] = query
            for page in range(1, pages + 1):
                params = params.copy()
                params.update({self._PAGE_KWORD: page})
                request_list.append(grequests.get(self.SEARCH_ENDPOINT, params=params, headers=self.HEADERS))
        return request_list

    def __str__(self) -> str:
        return 'shodan'
