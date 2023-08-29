class CountryDto:
    def __init__(self, name: str, code: str, code_3: str, latitude: float, longitude: float) -> None:
        self.name = name
        self.code = code
        self.code_3 = code_3
        self.latitude = latitude
        self.longitude = longitude
