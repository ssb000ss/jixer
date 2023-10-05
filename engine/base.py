import logging
import math
import os
import time
from http import HTTPStatus
import grequests
import requests

from utils.exceptions import NullResultException
from utils.helper import ipv4_sort


class BaseApiClient():
    """
        Base class for the API engine.

        Attributes:
            api_key (str): API key for the engine.
            _MAX_RETRY_ATTEMPTS (int): Maximum number of retry attempts.
            _RESULTS_PER_PAGE (int): Number of results per page.
            _TOTAL_ITEMS_KWORD (str): Key to retrieve the total number of items in the API response.
            BASE_URL (str): Base URL for API requests.
            COUNT_ENDPOINT (str): Endpoint for counting items.
            SEARCH_ENDPOINT (str): Endpoint for search queries.
            PARAMS (dict): Request parameters.
            HEADERS (dict): Request headers.
            _QUERY_KWORD (str): Key for passing search queries.
            _COUNT_KWORD (str): Key to retrieve the count in the API response.
            _IP_KWORD (str): Key to extract IP addresses from the API response.
            _PAGE_KWORD (str): Key for passing the page.
    """

    def __init__(self, api_key):
        """
             Initializes the BaseApiClient object.

             Args:
                 api_key (str): API key for the client.
        """
        self._MAX_RETRY_ATTEMPTS = 10
        self._RESULTS_PER_PAGE = 100
        self._TOTAL_ITEMS_KWORD = ''
        self.BASE_URL = ''
        self.COUNT_ENDPOINT = ''
        self.SEARCH_ENDPOINT = ''
        self.PARAMS = {}
        self.HEADERS = {}
        self._PAGE_KWORD = 'page'
        self._QUERY_KWORD = ''
        self._COUNT_KWORD = ''
        self._IP_KWORD = ''
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def count(self, query: str) -> int:
        """
          Get the number of items for a query.

          Args:
              query (str): Search query.

          Returns:
              int: Number of items matching the query.
        """
        params_copy = self.PARAMS.copy()
        params_copy[self._QUERY_KWORD] = query
        try:
            self.logger.info(f'Getting the number of servers for query: {query}')
            result = grequests.get(self.COUNT_ENDPOINT, params=params_copy, headers=self.HEADERS).send()
            if result.response.status_code == HTTPStatus.OK:
                count = result.response.json()[self._COUNT_KWORD]
                self.logger.info(f'For your query: [{query}], found [{count}]')
                return count
            else:
                self.logger.error(f'HTTP error: {result.responses.status_code}')
                self.logger.error(f'Error text: {result.responses.text}')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Error while making the request: {str(e)}')
        except Exception as e:
            self.logger.error(f'An unhandled error occurred: {str(e)}')

    def get_page_count(self, count: int) -> int:
        """
        Calculate the number of pages based on the total number of items.

        Args:
            count (int): Total number of items.

        Returns:
            int: Number of pages.
        """
        return math.ceil(count / self._RESULTS_PER_PAGE)

    def _search(self, query: str, count: int) -> list[str]:
        """
        Execute a search query to the API.

        Args:
            query (str): Search query.
            count (int): Number of items matching the query.

        Returns:
            list[str]: List of search results.
        """
        request_list = self.get_request_page_list(query, count)
        results = []
        for request in request_list:
            for retry in range(1, self._MAX_RETRY_ATTEMPTS):
                try:
                    self.logger.info(f'Sending a request: {query}, Parameters: {request.kwargs}')
                    result = request.send()
                    if result.response.status_code == HTTPStatus.OK:
                        page_results = result.response.json()[self._TOTAL_ITEMS_KWORD]
                        if len(page_results) > 0:
                            results.extend(page_results)
                            break
                        else:
                            raise NullResultException
                    else:
                        self.logger.error(f'HTTP error: {result.response.status_code}')
                        self.logger.error(f'Error text: {result.response.text}')
                except (
                        NullResultException, requests.exceptions.Timeout,
                        requests.exceptions.RequestException) as e:
                    if isinstance(e, NullResultException):
                        self.logger.error(f'Failed to retrieve the list of IP addresses from the API: {e}')
                    if retry < self._MAX_RETRY_ATTEMPTS - 1:
                        self.logger.warning(
                            f'Retrying the request in {retry} seconds (attempt {retry} of {self._MAX_RETRY_ATTEMPTS})')
                        time.sleep(retry)
                    else:
                        self.logger.error(f'Failed to get results after {retry} attempts')
        return results

    def search(self, query: str, count: int) -> list[str]:
        result_list = self._search(query, count)
        servers = self.get_parsed_ip_list(result_list)
        return ipv4_sort(servers)

    def get_ip_list(self, query: str, count) -> list[str]:
        results = self.search(query, count)
        if results:
            return self.get_parsed_ip_list(results)

    def get_request_page_list(self, query: str, count: int) -> list:
        """
        Get a list of requests for paging the results.

        Args:
            query (str): Search query.
            count (int): Number of items matching the query.

        Returns:
            list[grequests.Request]: List of requests for searching by pages.
        """
        raise NotImplementedError

    def get_parsed_ip_list(self, results: str) -> list:
        """
        Get a list of IP addresses from the search results.

        Args:
            results: Search results.

        Returns:
            list[str]: List of IP addresses.
        """
        raise NotImplementedError
