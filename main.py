from dotenv import load_dotenv
from view.view import View
from view.menu_item_dto import MenuItemDto
from database.migration import Migration
from service.country_service import CountryService
from service.gather_proxy_service import GatherProxyService
from service.gather.link_proxy_gather_service import LinkProxyGatherService
import sys
import os

load_dotenv()


def banner() -> str:
    with (open('resources/banner.txt', 'r') as banner_file):
        return View.paint(banner_file.read()) \
            .replace('{VERSION}', os.getenv('VERSION')) \
            .replace('{AUTHOR}', os.getenv('AUTHOR_NAME')) \
            .replace('{EMAIL}', os.getenv('AUTHOR_EMAIL')) \
            .replace('\\t', '\t')


def run_migration():
    View.separator()

    question: str = ('\t{Yellow}Are you sure that want run migration? '
                     '{BYellow}Previous database with all data will remove.'
                     '\n\t{Red}[{Cyan}y{ColorOff}/{BCyan}N{Red}]{ColorOff} -> ')

    if (
            '-y' not in sys.argv and
            (input(View.paint(question)) or 'N') not in ['Y', 'y']
    ):
        return

    migration = Migration()
    migration.run()
    View.separator()
    country_service = CountryService()
    country_service.seed_countries()
    View.separator()


def run_gather():
    View.separator()
    gather = GatherProxyService(LinkProxyGatherService())
    gather.run()
    print(View.paint('\t\t{Cyan}Saved new IPs {ColorOff}>> {BGreen}%d') % gather.get_count_saved())
    print(View.paint('\t\t{Cyan}Duplicates IPs {ColorOff}>> {BRed}%d') % gather.get_count_duplicates())
    View.separator()


def call_second():
    print('I\'m Second function!')


def main():
    View([
        MenuItemDto('Run Migration Database', 'migrate', run_migration),
        MenuItemDto('Gather IP from sources', 'link-gather', run_gather),
        MenuItemDto('Found IP via ProxyBroker', 'second', call_second),
        MenuItemDto('Check New proxies', 'test', call_second)
    ], banner())


if __name__ == "__main__":
    main()
