# Cards, Memes and Cats

You are used to watching ready-made memes. 
So can you create your own and compete with your friends? 
Could you post a card with a meme on the task that will make your friends laugh so loud they could be heard on Mars? 
Check it out in the game Cards, Memes and Cats.

## Api Reference

### Open Methods

Open endpoints require no Authentication

- [Room List](./docs/room_list.md): ``GET: /api/v0/room/list`` 
- [Create Room](./docs/create_room.md): ``POST: /api/v0/room/create`` 
- [Join Room](./docs/join_room.md): ``POST: /api/v0/room/join`` 

### Player Related

Closed endpoints require a valid Token to be included in the header of the request. 
A Token can be acquired via Joining the Room.

- [Leave Room](./docs/leave_room.md): ``POST: /api/v0/room/leave`` 
- [Start Game](./docs/start_game.md): ``POST: /api/v0/room/start`` 
- [Make Move](./docs/make_move.md): ``POST: /api/v0/game/move`` 


### WebSocket

WebSocket is using to push back all game events

- [Subscribe](./docs/subscribe.md): ``WS: /api/v0/game/subscribe/{token}`` 
