JOIN_MESSAGE = """JOIN_CHATROOM: {chatroom}
CLIENT_IP: 0
PORT: 0
CLIENT_NAME: {handle}
"""
CLIENT_JOINED_MESSAGE = """CLIENT_JOINED:{}"""
LEAVE_MESSAGE = """
LEAVE_CHATROOM: {room_ref}
JOIN_ID: {client_id}
CLIENT_NAME: {handle}
"""


DISCONNECT_MESSAGE = """DISCONNECT: 0
PORT: 0
CLIENT_NAME:{handle}
"""

JOINED_CHATROOM_MESSAGE = """JOINED_CHATROOM:{chatroom}
SERVER_IP:{server_ip}
PORT:{server_port}
ROOM_REF:{room_ref}
JOIN_ID:{client_id}
"""

LEFT_CHATROOM_MESSAGE = """LEFT_CHATROOM:{room_ref}
JOIN_ID:{client_id}
"""

SEND_MESSAGE = """CHAT:{room_ref}
CLIENT_NAME:{handle}
MESSAGE:{message} \n\n
"""

ERROR_MESSAGE = """ERROR_CODE: {code}
ERROR_DESCRIPTION: {description}"""
