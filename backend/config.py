import asyncio
import asyncpg
from aiohttp import web
from aiohttp_middlewares import cors_middleware
from queries import get_product_info
from crawling import scheduler


async def init_db(app):
    app['pool'] = await asyncpg.create_pool(
        database='ingredients',
        # host='collector',
        host='localhost',
        user='collector',
        password='c011lect',
        port=5432
    )
    yield
    app['pool'].close()


async def background_tasks(app):
    app['function_to_schedule'] = asyncio.create_task(
        scheduler()
    )
    yield
    app['function_to_schedule'].cancel()
    await app['function_to_schedule']

def init_app():
    app = web.Application(
        middlewares=[
            cors_middleware(
                allow_all=True,
                origins='*',
                allow_credentials=True,
                expose_headers='*',
                allow_headers='*',
                allow_methods=['GET']
            )
        ]
    )
    app.cleanup_ctx.append(init_db)
    app.cleanup_ctx.append(background_tasks)

    app.router.add_route('GET', '/', get_product_info)
    app.router.add_route('GET', '/{product:.*}', get_product_info)
    return app

