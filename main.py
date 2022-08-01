import logging
import os
import sys

from aiohttp import web

from game.api import route

logging.basicConfig(
    format="%(asctime)s | %(levelname)7s | %(name)16s | %(module)s.%(funcName)s.%(lineno)d: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)


async def create_app():
    app = web.Application()
    app.add_routes(route.routes)
    return app


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    web.run_app(create_app(), port=port)
