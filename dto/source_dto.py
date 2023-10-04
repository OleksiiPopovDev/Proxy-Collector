from datetime import datetime


class SourceDto:
    def __init__(
            self,
            url: str,
            hashsum: str = None,
            workable: bool = True,
            updated_at: datetime = datetime.now
    ) -> None:
        self.url: str = url
        self.hashsum: str = hashsum
        self.workable: bool = workable
        self.update_at: datetime = updated_at
