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
