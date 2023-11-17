import asyncio
from typing import Union, Any
import aiohttp
import time
import json
import math
from alive_progress import alive_bar
from repository.proxy_repository import ProxyRepository
from repository.status_repository import StatusRepository
from bash_menu_builder import Draw
from dto.status_dto import StatusDto
from dto.country_dto import CountryDto
from dto.proxy_dto import ProxyDto
from database.enum.proxy_status import ProxyStatus
import os


class CheckerService:
    def __init__(self):
        self.proxy_repository = ProxyRepository()
        self.pack: int = int(os.getenv('NUM_PROXIES_IN_CHECK_BATCH'))
        self.timeout: int = int(os.getenv('PROXY_RESPONSE_TIMEOUT'))
        self.show_success_result: bool = bool(int(os.getenv('SHOW_ONLY_SUCCESS_RESULT')))
        self.tries_limit: int = int(os.getenv('LIMIT_TRIES_CHECK_PROXY'))

    def run(self) -> None:
        count: int = self.proxy_repository.get_unchecked_count(self.tries_limit)
        iterates: int = math.ceil(count / self.pack)

        with alive_bar(count) as self.bar:
            for iteration in range(1, iterates + 1):
                string: str = Draw.paint('\t{Yellow}Pack {BYellow}%d {Red}[{Yellow}%d from %d{Red}]{ColorOff}')
                self.bar.title(string % (iteration, (iteration * self.pack), count))
                asyncio.run(self.check(iteration))

    async def check(self, iteration: int, **kwargs) -> tuple[Union[BaseException, Any]]:
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            proxies = self.proxy_repository.get_unchecked(
                tries_limit=self.tries_limit,
                limit=self.pack,
                iteration=iteration
            )

            for proxy in proxies:
                tasks.append(self.send_request(session=session, ip=proxy.ip, port=proxy.port, **kwargs))

            return await asyncio.gather(*tasks, return_exceptions=True)

    async def send_request(self, session: aiohttp.ClientSession, ip: str, port: int, **kwargs) -> None:
        proxy = '%s:%d' % (ip, port)
        proxy_url = 'http://%s' % proxy
        url = 'https://api.myip.com'
        spaces_count: int = 25 - len(proxy)

        try:
            start_time = time.time()
            resp = await session.get(url=url, proxy=proxy_url, **kwargs)
        except Exception as message:
            if not self.show_success_result:
                print(
                    Draw.paint('{Yellow}[{Red}-{Yellow}]{ColorOff} %s%s => %s') %
                    (proxy, (' ' * spaces_count), (message if not isinstance(message, TimeoutError) else message))
                )

            status = StatusDto(
                ip=ProxyDto(ip=ip, port=port),
                country=CountryDto(name=None),
                is_working=False,
                status=ProxyStatus.INVALID,
                response=str(message)
            )
        else:
            data = await resp.read()
            json_data = json.loads(data)
            time_count = time.time() - start_time
            spaces_count_2 = 25 - len(str(time_count))
            print(
                Draw.paint(
                    '{Yellow}[{BGreen}+{Yellow}]{Green} %s%s {ColorOff}=> Time: {Blue}%s%s {ColorOff}Response: %s') %
                (proxy, (' ' * spaces_count), time_count, (' ' * spaces_count_2), json_data)
            )

            status = StatusDto(
                ip=ProxyDto(ip=ip, port=port),
                country=CountryDto(name=json_data['country'], code=json_data['cc']),
                is_working=True,
                status=ProxyStatus.VALID,
                response_time=time_count,
                response=json_data
            )

        try:
            StatusRepository.save(status)
        except Exception as message:
            print(message)
        self.bar()
