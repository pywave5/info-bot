from html import escape
from dataclasses import dataclass

from a2s import ainfo, aplayers
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=60)

IMAGE_URL = "https://image.gametracker.com/images/maps/160x120/cs/"

@dataclass
class Ainfo:
    servers: list[dict]

    async def get_server_info(self, servers: list[dict]) -> list[dict]:
        answers = []
        for server in servers:
            ip_port = (server["ip"], server["port"])

            cached_info = cache.get(ip_port)
            if cached_info:
                result, players = cached_info
            else:
                result = await ainfo((server["ip"], server["port"]))
                players = await aplayers((server["ip"], server["port"]))

            if result:
                server_name: str = result.server_name
                map_name: str = result.map_name
                player_count: int = result.player_count
                max_players: int = result.max_players
                bot_count: int = result.bot_count
                image_url: str = f"{IMAGE_URL}{map_name}.jpg"

                players_caption = "# | Nick | Score | Time" if player_count > 0 else ""
                for idx, player in enumerate(players):
                    playerName = escape(s=player.name, quote=True)
                    playerTime = player.duration
                    playerScore = player.score
                    minutes = int(playerTime // 60)
                    seconds = round((playerTime % 60))
                    players_caption += f'\n{idx + 1}. <code>🥷🏻{playerName} | 🔫{playerScore} | 🕒{minutes}:{seconds}</code>'

                answer = {
                    "host": f"{server['ip']}:{server['port']}",
                    "server_name": server_name,
                    "map_name": map_name,
                    "player_count": player_count,
                    "max_players": max_players,
                    "bot_count": bot_count,
                    "image_url": image_url,
                    "players_caption": players_caption
                }
                answers.append(answer)

        return answers
