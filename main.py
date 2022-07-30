import aiohttp
from aiohttp import web, WSMessage


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        msg: WSMessage = msg
        print(msg)

        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


application = web.Application()
application.add_routes([
    web.get('/ws', websocket_handler)
])

# web.run_app(application)
