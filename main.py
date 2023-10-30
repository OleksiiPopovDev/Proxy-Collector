import getopt
import re
from dotenv import load_dotenv
from bash_menu_builder import SelectMenu, MenuItemDto, Draw
from database.migration import Migration
from service.country_service import CountryService
from service.source_service import SourceService
from service.gather_proxy_service import GatherProxyService
from service.checker_service import CheckerService
from service.gather.link_proxy_gather_service import LinkProxyGatherService
from service.gather.broker_proxy_gather_service import BrokerProxyGatherService
import sys
import os

load_dotenv()


def banner() -> str:
    with (open('resources/banner.txt', 'r') as banner_file):
        return Draw.paint(banner_file.read()) \
            .replace('{VERSION}', os.getenv('VERSION')) \
            .replace('{AUTHOR}', os.getenv('AUTHOR_NAME')) \
            .replace('{EMAIL}', os.getenv('AUTHOR_EMAIL')) \
            .replace('\\t', '\t')


def run_migration():
    Draw.separator()

    question: str = ('\t{Yellow}Are you sure that want run migration? '
                     '{BYellow}Previous database with all data will remove.'
                     '\n\t{Red}[{Cyan}y{ColorOff}/{BCyan}N{Red}]{ColorOff} -> ')

    if (
            '-y' not in sys.argv and
            (input(Draw.paint(question)) or 'N') not in ['Y', 'y']
    ):
        return

    migration = Migration()
    migration.run()
    Draw.separator()
    country_service = CountryService()
    country_service.seed_countries()
    Draw.separator()


def run_source_validator():
    Draw.separator()
    source = SourceService()
    source.seed_sources()
    Draw.separator()


def run_gather():
    Draw.separator()
    gather = GatherProxyService(LinkProxyGatherService())
    gather.run()
    print(Draw.paint('\t\t{Cyan}Saved new IPs {ColorOff}>> {BGreen}%d') % gather.get_count_saved())
    print(Draw.paint('\t\t{Cyan}Duplicates IPs {ColorOff}>> {BRed}%d') % gather.get_count_duplicates())
    Draw.separator()


def run_proxybroker():
    compile_re = re.compile('-count=\d+')
    search_list = list(filter(compile_re.match, sys.argv))
    if len(search_list) == 0:
        question: str = ('\t{Yellow}How many Proxies IPs search? '
                         '\n\t{Red}[{ColorOff}Default: {BCyan}100{Red}]{ColorOff} -> ')
        try:
            count = int(input(Draw.paint(question))) or 100
        except ValueError:
            count = 100
    else:
        count_str = search_list[0].split('=')
        count: int = int(count_str[1])

    count = count if count <= 1000 else 1000
    broker = BrokerProxyGatherService()
    broker.set_limit(count)
    gather = GatherProxyService(broker)
    gather.run()


def run_checker():
    checker = CheckerService()
    checker.run()


if __name__ == "__main__":
    #print(getopt.getopt(sys.argv[1:], 'a:b:c', ['letter-a=', 'letter-b=', 'letter-c=']))
    #exit()
    SelectMenu(
        banner=banner(),
        menu=[
            MenuItemDto(title='Run Migration Database', option='migrate', handler=run_migration),
            MenuItemDto(title='Refresh Sources', option='refresh-sources', handler=run_source_validator),
            MenuItemDto(title='Gather IP from sources', option='link-gather', handler=run_gather),
            MenuItemDto(title='Found IP via ProxyBroker', option='broker-gather', handler=run_proxybroker),
            MenuItemDto(title='Check New proxies', option='check', handler=run_checker)
        ]
    )
