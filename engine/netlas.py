from urllib.parse import urljoin

import grequests

from engine.base import BaseApiClient


class NetlasClient(BaseApiClient):
    """
    Клиент для работы с API Netlas.

    Attributes:
        BASE_URL (str): Базовый URL для API-запросов Netlas.
        COUNT_ENDPOINT (str): Конечная точка для запроса количества элементов.
        SEARCH_ENDPOINT (str): Конечная точка для поисковых запросов.
        HEADERS (dict): Заголовки для запросов к API.
        PARAMS (dict): Параметры запроса API.
        _IP_KWORD (str): Ключ для извлечения IP-адресов из результатов.
        _COUNT_KWORD (str): Ключ для получения количества элементов в ответе API.
        _QUERY_KWORD (str): Ключ для передачи поискового запроса.
        _RESULTS_PER_PAGE (int): Количество результатов на одной странице.
        _TOTAL_ITEMS_KWORD (str): Ключ для получения общего количества элементов в ответе API.
    """

    def __init__(self, api_key):
        """
        Инициализация объекта NetlasClient.

        Args:
            api_key (str): API-ключ клиента.
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
        Получение списка запросов для разбивки результатов по страницам.

        Args:
            query (str): Поисковый запрос.
            count (int): Количество элементов, удовлетворяющих запросу.

        Returns:
            list[grequests.Request]: Список запросов для поиска по страницам.
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
        Извлечение IP-адресов из результатов запроса.

        Args:
            results: Результаты запроса.

        Returns:
            set[str]: Множество IP-адресов.
        """
        return set([_.get('data').get('ip') for _ in results])

    def __str__(self):
        return 'netlas'
