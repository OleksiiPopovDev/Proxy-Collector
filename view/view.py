from view.menu_item_dto import MenuItemDto
from view.color import Color
import signal
import sys


class View:
    def __init__(self, menu: list[MenuItemDto], banner: str = None) -> None:
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        self.__menu_items = menu
        self.__check_options()
        if banner:
            print(banner)

        self.show_menu()

    def __check_options(self):
        for menu_item in self.__menu_items:
            option = '--%s' % menu_item.option_name
            if option in sys.argv:
                self.__call_handler(menu_item.handler)

    def show_menu(self) -> None:
        print(Color.ColorOff.value)
        count: int = 1
        for item in self.__menu_items:
            print(self.paint("\t\t{Red}[{Yellow}%d{Red}]\t{Cyan} %s" % (count, item.title)))
            count += 1

        print(self.paint("\t\t\t {Purple}For {UPurple}Exit{Purple} press {BPurple}Ctrl+C{ColorOff}\n"))
        self.__propose_choose()

    def __propose_choose(self) -> None:
        try:
            selected_menu = int(input(self.paint("\t\t{Green}Choose menu number {BGreen}>> "))) - 1
            menu_item = self.__menu_items[selected_menu]
            self.__call_handler(menu_item.handler)

        except (RuntimeError, ValueError, KeyboardInterrupt, IndexError):
            print(self.paint('\t\t{BRed}Error: {Red} Incorrect selected menu!{ColorOff}\n'))
            self.__propose_choose()

    def __call_handler(self, handler) -> None:
        if not callable(handler):
            raise RuntimeError('Item has incorrect Callable type. Please, ask developer fix it!')

        handler()
        self.show_menu()

    @staticmethod
    def separator() -> None:
        print("%s-" % Color.ColorOff.value * 100)

    @staticmethod
    def paint(string: str) -> str:
        for color in Color:
            string = string.replace("{%s}" % color.name, color.value)

        return string

    @staticmethod
    def count_biggest_line(list_items: list) -> int:
        biggest_line_length: int = 0
        for item in list_items:
            name_length = len(item)
            biggest_line_length = name_length if name_length > biggest_line_length else biggest_line_length

        return biggest_line_length

    @staticmethod
    def add_spaces_for_line_up(line: str, count_biggest_line: int) -> str:
        more_spaces: int = count_biggest_line - len(line)
        return line + ' ' * more_spaces

    @staticmethod
    def get_count_spaces_for_line_up(line: str, count_biggest_line: int) -> int:
        return count_biggest_line - len(line)
