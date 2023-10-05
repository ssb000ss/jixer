class NullResultException(Exception):
    def __init__(self):
        super().__init__('Number of results should be greater than zero')
