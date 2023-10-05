import base64
import os
import logging

from datetime import datetime

logger = logging.getLogger(__name__)


def query_to_bs64(query_str: str) -> str:
    """
    Encodes a query string in Base64 format.

    Args:
        query_str (str): The query string to encode.

    Returns:
        str: The encoded string in Base64 format.
    """
    encoded_query = query_str.encode()
    encoded_query = base64.b64encode(encoded_query)
    return encoded_query.decode()


def ipv4_sort(ip_list):
    """
    Sort a list of IPV4 addresses.
    Args:
        ip_list (list): A list of IPV4 addresses.

    Returns:
        list : A sorted list of IPV4 addresses.
    """

    def ip_key(ip):
        parts = ip.split('.')
        return [int(part) for part in parts]

    return sorted(ip_list, key=ip_key)


def save_results(query: str, servers: list[str], file_name='', folder_name='results') -> bool:
    """
    Save search results to a file.

    Args:
        query (str): Search query.
        servers (list[str]): List of IP addresses to save.
        file_name (str): File name to save results to.
        folder_name (str): Folder name to save results.

    Returns:
        bool: True if the results were successfully saved, False in case of an error.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if not file_name:
        current_datetime = datetime.now()
        file_name = f'{current_datetime.strftime("%Y_%m_%d_%H_%M_%S")}.txt'
    file_path = f'{folder_name}/{file_name}'
    try:
        with open(file_path, 'w') as file:
            for server in servers:
                file.write(server + '\n')
        logger.info(
            f'Results for the query {query} were successfully written to the file "{file_path}".')
        return True
    except IOError as e:
        logger.error(f'An error occurred while writing results to the file: {e}')
