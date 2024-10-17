import os
import json

class JsonFileHandler:
    def __init__(self, file_name: str):
        self.file_name = file_name

    async def save_command(self, command: str, description: str) -> None:
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="UTF-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        for cmd_data in data.values():
            if cmd_data['command'] == command:
                return

        command_id = str(len(data) + 1)
        data[command_id] = {"command": command, "description": description}

        with open(self.file_name, "w", encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    async def load_commands(self) -> dict:
        if not os.path.exists(self.file_name):
            return {}

        with open(self.file_name, "r", encoding="UTF-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return {}

        return data

    async def delete_command(self, command: str) -> None:
        if not os.path.exists(self.file_name):
            return

        with open(self.file_name, "r", encoding="UTF-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return

        key_to_delete = None
        for key, cmd_data in data.items():
            if cmd_data['command'] == command:
                key_to_delete = key
                break

        if key_to_delete:
            del data[key_to_delete]

            with open(self.file_name, "w", encoding="UTF-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)