class CountryDto:
    def __init__(
            self,
            id: int = None,
            name: str = None,
            code: str = None,
            code_3: str = None,
            latitude: float = None,
            longitude: float = None
    ) -> None:
        self.id: int = id
        self.name = name
        self.code = code
        self.code_3 = code_3
        self.latitude = latitude
        self.longitude = longitude
