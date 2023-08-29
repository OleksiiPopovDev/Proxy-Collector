class MenuItemDto:
    def __init__(self, title: str, option_name: str, handler: object):
        self.title: str = title
        self.option_name: str = option_name.replace(' ', '')
        self.handler: object = handler
