# import aiohttp
# from aiohttp import web, WSMessage
#
#
# async def websocket_handler(request):
#     ws = web.WebSocketResponse()
#     await ws.prepare(request)
#
#     async for msg in ws:
#         msg: WSMessage = msg
#         print(msg)
#
#         if msg.type == aiohttp.WSMsgType.TEXT:
#             if msg.data == 'close':
#                 await ws.close()
#             else:
#                 await ws.send_str(msg.data + '/answer')
#         elif msg.type == aiohttp.WSMsgType.ERROR:
#             print('ws connection closed with exception %s' %
#                   ws.exception())
#
#     print('websocket connection closed')
#
#     return ws
#
#
# async def hello(request):
#     return web.Response(text="Hello, world")
#
#
# application = web.Application()
# application.add_routes([
#     # web.get('/ws', websocket_handler)
#     web.get('/', hello)
# ])
#
# web.run_app(application)

import os
from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


async def create_app():
    app = web.Application()
    app.add_routes([
        # web.get('/ws', websocket_handler)
        web.get('/', hello)
    ])
    return app


# If running directly https://docs.aiohttp.org/en/stable/web_quickstart.html
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    web.run_app(create_app(), port=port)
