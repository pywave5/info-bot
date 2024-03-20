from dataclasses import dataclass
import a2s

URL = "https://image.gametracker.com/images/maps/160x120/cs/"

def escape_string(str):
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")

    return str

@dataclass
class Ainfo:
    servers: list[dict]

    async def get_server_info(self, servers: list[dict]) -> list[dict]:
        answers = []
        for server in servers:
            result = await a2s.ainfo((server["ip"], server["port"]))
            players = await a2s.aplayers((server["ip"], server["port"]))

            if result:
                server_name: str = result.server_name
                map_name: str = result.map_name
                player_count: int = result.player_count
                max_players: int = result.max_players
                bot_count: int = result.bot_count
                image_url = f"{URL}{map_name}.jpg"

                players_caption = "# | Nick | Score | Time"
                for idx, player in enumerate(players):
                    playerName = escape_string(player.name)
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