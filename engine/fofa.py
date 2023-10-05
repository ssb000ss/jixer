from urllib.parse import urljoin

import grequests

from engine.base import BaseApiClient
from utils.helper import query_to_bs64


class FofaClient(BaseApiClient):
    """
    Клиент для работы с API Fofa.

    Attributes:
        BASE_URL (str): Базовый URL для API-запросов Fofa.
        COUNT_ENDPOINT (str): Конечная точка для запроса количества элементов.
        SEARCH_ENDPOINT (str): Конечная точка для поисковых запросов.
        _COUNT_KWORD (str): Ключ для получения количества элементов в ответе API.
        _QUERY_KWORD (str): Ключ для передачи поискового запроса в кодировке Base64.
        _RESULTS_PER_PAGE (int): Количество результатов на одной странице.
        _TOTAL_ITEMS_KWORD (str): Ключ для получения общего количества элементов в ответе API.
        PARAMS (dict): Параметры запроса API.
    """

    def __init__(self, api_key: str, email: str):
        """
        Инициализация объекта FofaClient.

        Args:
            api_key (str): API-ключ клиента.
            email (str): Адрес электронной почты клиента.
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
        Извлекает IP-адреса из результатов запроса.

        Args:
            results: Результаты запроса.

        Returns:
            set[str]: Множество IP-адресов.
        """
        return set([_[1] for _ in results])

    def count(self, query: str) -> int:
        """
        Получение количества элементов, удовлетворяющих запросу.

        Args:
            query (str): Поисковый запрос.

        Returns:
            int: Количество элементов, удовлетворяющих запросу.
        """
        query_b64 = query_to_bs64(query)
        return super().count(query_b64)

    def get_request_page_list(self, query: str, count: int) -> list:
        """
        Получение списка запросов для разбивки результатов по страницам.

        Args:
            query (str): Поисковый запрос.
            count (int): Количество элементов, удовлетворяющих запросу.

        Returns:
            list[grequests.Request]: Список запросов для поиска по страницам.
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
