from . import handlers

routes = [
    # Public Methods
    handlers.index,
    handlers.create_room,
    handlers.join_room,
    handlers.room_list,

    # Player Methods
    handlers.leave_room,
    handlers.start_game,
    handlers.make_move,

    # Websocket
    handlers.subscribe
]
