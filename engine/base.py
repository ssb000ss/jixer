import logging
import math
import os
import time
from datetime import datetime
from http import HTTPStatus
import grequests
import requests

from utils.exceptions import NullResultException


class BaseApiClient():
    """
        Базовый класс для API-движка.

        Атрибуты:
            api_key (str): API-ключ движка.
            _MAX_RETRY_ATTEMPTS (int): Максимальное количество попыток повторной отправки запроса.
            _RESULTS_PER_PAGE (int): Количество результатов на одной странице.
            _TOTAL_ITEMS_KWORD (str): Ключ для получения общего количества элементов в ответе API.
            BASE_URL (str): Базовый URL для API-запросов.
            COUNT_ENDPOINT (str): Конечная точка для запроса количества элементов.
            SEARCH_ENDPOINT (str): Конечная точка для поисковых запросов.
            PARAMS (dict): Параметры запроса.
            HEADERS (dict): Заголовки запроса.
            _QUERY_KWORD (str): Ключ для передачи поискового запроса.
            _COUNT_KWORD (str): Ключ для получения количества элементов в ответе API.
            _IP_KWORD (str): Ключ для извлечения IP-адресов из ответа API.
            _PAGE_KWORD (str): Ключ для передачи страницы
    """

    def __init__(self, api_key):
        """
             Инициализация объекта BaseApiClient.

             Args:
                 api_key (str): API-ключ клиента.
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
          Получение количества элементов по запросу.

          Args:
              query (str): Поисковый запрос.

          Returns:
              int: Количество элементов, удовлетворяющих запросу.
        """
        params_copy = self.PARAMS.copy()
        params_copy[self._QUERY_KWORD] = query
        try:
            self.logger.info(f'Получение количество серверов по запросу: {query}')
            result = grequests.get(self.COUNT_ENDPOINT, params=params_copy, headers=self.HEADERS).send()
            if result.response.status_code == HTTPStatus.OK:
                count = result.response.json()[self._COUNT_KWORD]
                self.logger.info(f'По вашему запросу: [{query}], найдено [{count}]')
                return count
            else:
                self.logger.error(f'Ошибка HTTP: {result.responses.status_code}')
                self.logger.error(f'Текст ошибки: {result.responses.text}')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Ошибка при выполнении запроса: {str(e)}')

        except Exception as e:
            self.logger.error(f'Произошла необрабатываемая ошибка: {str(e)}')

    def get_page_count(self, count: int) -> int:
        """
        Вычисление количества страниц на основе общего количества элементов.

        Args:
            count (int): Общее количество элементов.

        Returns:
            int: Количество страниц.
        """
        return math.ceil(count / self._RESULTS_PER_PAGE)

    def _search(self, query: str, count: int) -> list[str]:
        """
        Выполнение поискового запроса к API.

        Args:
            query (str): Поисковый запрос.
            count (int): Количество элементов, удовлетворяющих запросу.

        Returns:
            list[str]: Список результатов поиска.
        """
        request_list = self.get_request_page_list(query, count)
        results = []
        for request in request_list:
            for retry in range(1, self._MAX_RETRY_ATTEMPTS):
                try:
                    self.logger.info(f'Отправка запроса: {query}, Параметры: {request.kwargs}')
                    result = request.send()
                    if result.response.status_code == HTTPStatus.OK:
                        page_results = result.response.json()[self._TOTAL_ITEMS_KWORD]
                        if len(page_results) > 0:
                            results.extend(page_results)
                            break
                        else:
                            raise NullResultException
                    else:
                        self.logger.error(f'Ошибка HTTP: {result.response.status_code}')
                        self.logger.error(f'Текст ошибки: {result.response.text}')

                except (
                        NullResultException, requests.exceptions.Timeout,
                        requests.exceptions.RequestException) as e:
                    if isinstance(e, NullResultException):
                        self.logger.error(f'Не удалось получить список IP-адресов из API: {e}')
                    if retry < self._MAX_RETRY_ATTEMPTS - 1:
                        self.logger.warning(
                            f'Переотправляем запрос через {retry} секунду (попытка {retry} из {self._MAX_RETRY_ATTEMPTS})')
                        time.sleep(retry)
                    else:
                        self.logger.error(f'Не удалось получить результат после {retry} попыток')
        return results

    def search(self, query: str, count: int) -> list[str]:
        result_list = self._search(query, count)
        servers = self.get_parsed_ip_list(result_list)
        return servers

    def get_ip_list(self, query: str, count) -> list[str]:
        results = self.search(query, count)
        if results:
            return self.get_parsed_ip_list(results)

    def save_results(self, query: str, servers: list[str]) -> bool:
        """
        Сохранение результатов поиска в файл.

        Args:
            query (str): Поисковый запрос.
            servers (list[str]): Список IP-адресов для сохранения.

        Returns:
            bool: True, если результаты успешно сохранены, False в случае ошибки.
        """
        folder_name = 'results'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        current_datetime = datetime.now()
        file_name = f'{folder_name}/{current_datetime.strftime("%Y_%m_%d_%H_%M_%S")}_{self}.txt'
        try:
            with open(file_name, 'w') as file:
                file.write(f'Results query:{query} for client {self} - {file_name}\n')
                for server in servers:
                    file.write(server + '\n')
            self.logger.info(
                f'Результаты по запроса {query} для клиента "{str(self)}", успешно записаны в файл "{file_name}".')
            return True
        except IOError as e:
            self.logger.error(f'Произошла ошибка при записи результатов в файл: {e}')

    def get_request_page_list(self, query: str, count: int) -> list:
        """
        Получение списка запросов для разбивки результатов по страницам.

        Args:
            query (str): Поисковый запрос.
            count (int): Количество элементов, удовлетворяющих запросу.

        Returns:
            list[grequests.Request]: Список запросов для поиска по страницам.
        """
        raise NotImplementedError

    def get_parsed_ip_list(self, results: str) -> list:
        """
        Получение списка IP-адресов из результатов поиска.

        Args:
            results: Результаты поиска.

        Returns:
            list[str]: Список IP-адресов.
        """
        raise NotImplementedError
