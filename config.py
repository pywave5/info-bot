"""
    info bot for your servers
    author: @pywave
    version: 3.0.0
"""

TOKEN_API = "BOT_TOKEN" # YOUR BOT TOKEN

# LIST YOUR GAME SERVERS
SERVERS = [
    {"ip": "127.0.0.1", "port": 27015},
    # {"ip": "127.0.0.1", "port": 27016}
]

# defines the delay time in seconds before messages are automatically deleted.
AUTO_DELETE_DELAY_TIME = 300

# If specified, the bot will restrict access to users who are not members of the group or channel.
CHAT_ID: int | None = None # Example: -1002281063512 (@username_to_id_bot)

# admins ids for your bot
ADMINS_IDS = [] # username_to_id_bot