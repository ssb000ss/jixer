class NullResultException(Exception):
    def __init__(self):
        super().__init__('Количество результатов должно быть больше нуля')
