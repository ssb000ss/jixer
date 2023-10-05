import base64


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
