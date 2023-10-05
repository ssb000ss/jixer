from urllib.parse import urljoin
import grequests
from engine.base import BaseApiClient


class ZoomeyeClient(BaseApiClient):
    """
    Клиент для работы с API ZoomEye.

    Attributes:
        BASE_URL (str): Базовый URL для API-запросов ZoomEye.
        COUNT_ENDPOINT (str): Конечная точка для запроса количества элементов.
        SEARCH_ENDPOINT (str): Конечная точка для поисковых запросов.
        HEADERS (dict): Заголовки для запросов к API.
        PARAMS (dict): Параметры запроса API.
        _QUERY_KWORD (str): Ключ для передачи поискового запроса.
        _COUNT_KWORD (str): Ключ для получения количества элементов в ответе API.
        _IP_KWORD (str): Ключ для получения IP-адресов из ответа API.
        _RESULTS_PER_PAGE (int): Максимальное количество результатов на странице.
        _TOTAL_ITEMS_KWORD (str): Ключ для получения общего количества элементов в ответе API.
    """

    def __init__(self, api_key: str):
        """
        Инициализация объекта ZoomeyeClient.

        Args:
            api_key (str): API-ключ клиента ZoomEye.
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
            params['query'] = query
            for page in range(1, pages + 1):
                params = params.copy()
                params.update({self._PAGE_KWORD: page})
                request_list.append(grequests.get(self.SEARCH_ENDPOINT, params=params, headers=self.HEADERS))
        return request_list

    def get_parsed_ip_list(self, results: list) -> set:
        """
        Извлечение IP-адресов из результатов запроса.

        Args:
            results (list): Результаты запроса.

        Returns:
            set[str]: Множество IP-адресов.
        """
        return set([_.get('ip') for _ in results])

    def __str__(self) -> str:
        return 'zoomeye'
