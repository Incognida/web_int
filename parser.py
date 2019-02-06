import argparse
import asyncio

from models import db_session, Result

from aiohttp import ClientSession


SEMA = asyncio.BoundedSemaphore(1000)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.json()


async def parse(url, session):
    async with SEMA:
        task = [asyncio.ensure_future(fetch(url, session))]
        response = await asyncio.gather(*task)
        result = Result(data=response)
        db_session.add(result)
        db_session.commit()
        db_session.refresh(result)


async def run(urls):
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(parse(url, session)))
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', dest='path', type=str, required=True)
    args = parser.parse_args()
    path = args.path

    urls = []
    for url in open(path):
        urls.append(url)

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(urls))
    loop.run_until_complete(future)
