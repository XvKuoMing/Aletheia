import asyncio
from aiohttp import web
from config import init_app
import asyncpg

# https://stackoverflow.com/questions/48926218/web-py-hello-world-not-working-err-address-invalid


app = init_app()
web.run_app(app)




