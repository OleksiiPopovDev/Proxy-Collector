class ProxyDto:
    def __init__(
            self,
            ip: str,
            port: int = 80,
            type: str = None,
            country: str = None,
            response_time: float = 0,
            tries: int = 0
    ) -> None:
        self.ip = ip
        self.port = port
        self.type = type
        self.country = country
        self.response_time = response_time
        self.tries = tries
