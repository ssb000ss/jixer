import base64


def query_to_bs64(query_str:str) -> str:
    """
    Кодирует строку запроса в формат Base64.

    Args:
        query_str (str): Строка запроса, которую нужно закодировать.

    Returns:
        str: Закодированная строка в формате Base64.
    """
    encoded_query = query_str.encode()
    encoded_query = base64.b64encode(encoded_query)
    return encoded_query.decode()
