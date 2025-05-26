# Info Bot — Telegram-бот для мониторинга CS 1.6 серверов

**Info Bot** — это асинхронный Telegram-бот на Python, который предоставляет информацию о серверах GoldSrc (например, CS 1.6) прямо в интерфейсе Telegram. Удобен для администраторов, геймеров и сообществ.

![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![Version](https://img.shields.io/badge/version-3.0.0-blue)
[![Telegram Chat](https://img.shields.io/badge/chat-Telegram-blue?logo=telegram)](https://t.me/pywave)
![Downloads](https://img.shields.io/github/downloads/pywave5/info-bot/total?label=downloads)

---

## Превью

![Пример карты](https://image.gametracker.com/images/maps/160x120/cs/de_dust2.jpg)  
*Бот отображает карту, название сервера, текущих игроков, счёт и многое другое.*

---

## Основные возможности

- **Мониторинг GoldSrc-серверов (CS 1.6)** — показывает название, карту, игроков, пинг и другие параметры.
- **Поддержка нескольких серверов** — можно добавить любое количество игровых серверов.
- **Добавление новых команд для пользователей в интерфейсе бота** — администратор может добавить свои команды интерфейс бота.
- **Кэширование запросов** — уменьшает нагрузку на сервера за счёт `TTLCache`.
- **Автоматическое удаление сообщений** — в группах бот удаляет инфо-сообщения через несколько секунд (настраивается), чтобы не засорять чат.
- **Проверка подписки** — доступ к боту возможен только для подписчиков определённого канала/группы.
- **Превью карты** — бот автоматически подставляет изображение карты из GameTracker.

---

## Установка

```bash
git clone https://github.com/pywave5/info-bot.git
cd info-bot
pip install -r requirements.txt
```

---

## Настройка

настройте `config.py`:
```
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
```
---

## Запуск

```bash
nohup python3 main.py &
```

---

## Зависимости

- Python 3.9+
- aiogram
- a2s
- cachetools

---

## Лицензия

[MIT License](LICENSE)
