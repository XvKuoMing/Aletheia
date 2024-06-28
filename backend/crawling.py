import asyncio

import schedule
import threading
import asyncpg
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from collector.spiders.crosser import CrosserSpider


def feed_spiders(products: list):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    CrosserSpider.products = products
    # SparSpider.products = products
    process.crawl(CrawlerProcess)
    process.start()  # https://www.geeksforgeeks.org/python-schedule-library/?ysclid=lxma15ewlc557868536


async def check_products():
    # if coming products, run feed spiders with those products
    conn = await asyncpg.connect(
        database='ingredients',
        host='localhost',
        user='collector',
        password='c011lect',
        port=5432
    )
    results = await conn.execute(
        """
        SELECT product FROM read_and_delete();
        """
    )
    products = [dict(record)['product'] for record in results]
    feed_spiders(products)


def run_scheduler():
    while True:
        schedule.run_pending()

async def scheduler():
    schedule.every(1).days.do(check_products)
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    while True:
        await asyncio.sleep(1)

