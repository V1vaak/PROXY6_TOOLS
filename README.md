# 🔌 Proxy6 Python Client

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![AIOHTTP](https://img.shields.io/badge/aiohttp-3.9+-blueviolet.svg)
![Requests](https://img.shields.io/badge/requests-2.31+-orange.svg)
![Async Support](https://img.shields.io/badge/Async-✅-brightgreen.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/V1vaak/PROXY6-Telegram-bot)

Полнофункциональный синхронный и асинхронный клиент для работы с API сервиса Proxy6.

## 📋 Содержание
- [🔗 Полезные ссылки](#полезные-ссылки)
- [⚙️ Установка](#установка)
- [🚀 Быстрый старт](#быстрый-старт)
- [Синхронный клиент](#синхронный-клиент)
- [Асинхронный клиент](#асинхронный-клиент)
- [🔧 Основные методы](#основные-методы)
- [📄 Лицензия](#лицензия)

### 🔗 Полезные ссылки

- [🌐 Официальный сайт Proxy6](https://px6.me/)
- [📚 Документация Proxy6 API](https://px6.me/ru/developers)
- [🔑 Получение API ключа](https://px6.me/ru/user/developers)
- [📚 Документация PyPI: requests](https://pypi.org/project/requests/)
- [📚 Документация PyPI: aiohttp](https://pypi.org/project/aiohttp/)


## ⚙️ Установка

```bash
# Клонирование репозитория
git clone https://github.com/V1vaak/proxy6-python-client.git
cd proxy6-python-client

# Устанавливаем зависимости
pip install -r requirements.txt
```

## 🚀 Быстрый старт

### Синхронный клиент
```python
from proxy6_client import Proxy6

# Инициализация клиента
client = Proxy6(api="ваш_api_ключ")

try:
    # Получение баланса
    info = client.info()
    print(f"Баланс: {info['balance']} руб.")
    
    # Покупка прокси
    proxies = client.buy(
        count=5,
        period=30,
        country="ru",
        version=4,
        type="socks",
        descr="Мои прокси"
    )
finally:
    # Закрытие сессии
    client.close()
```

### Асинхронный клиент
```python
import asyncio
from proxy6_client import AsyncProxy6

async def main():
    async with AsyncProxy6(api="ваш_api_ключ") as client:
        # Получение списка стран
        countries = await client.get_country(version=4)
        print(f"Доступные страны для IPv4: {countries}")
        
        # Получение активных прокси
        proxies = await client.get_proxy(state="active")
        print(f"Активных прокси: {len(proxies)}")

asyncio.run(main())
```

## Синхронный клиент (Proxy6)

### Инициализация
```python
from proxy6_client import Proxy6

client = Proxy6(api="ваш_api_ключ")
```

### Основные методы

#### Информационные методы
```python
# Получение баланса и информации об аккаунте
info = client.info()
print(f"Баланс: {info['balance']} руб.")
print(f"Статус: {info['status']}")
print(f"Скидка: {info.get('discount', 0)}%")

# Получение стоимости
price = client.get_price(count=10, period=30, version=4)
print(f"Стоимость 10 IPv4 прокси на 30 дней: {price} руб.")

# Проверка доступности
count = client.get_count(country="ru", version=4)
print(f"Доступно прокси в России: {count}")

# Список стран
countries = client.get_country(version=4)
print(f"Страны с IPv4: {countries}")
```

#### Управление прокси
```python
# Покупка прокси
proxies = client.buy(
    count=3,
    period=7,
    country="us",
    version=4,
    type="http",
    descr="Американские HTTPS",
    auto_prolong=True
)

# Получение списка прокси
all_proxies = client.get_proxy(state="all")
active_proxies = client.get_proxy(state="active", limit=50)
expiring_proxies = client.get_proxy(state="expiring")

# Изменение типа протокола
client.set_type(ids=(12345, 12346), type="socks")

# Обновление комментария
success, updated_count = client.set_descr(
    new="Обновленный комментарий",
    ids=(12345, 12346)
)

# Продление
client.prolong(period=30, ids=(12345, 12346))

# Удаление
client.delete(ids=12345)  # По ID
client.delete(descr="Старые прокси")  # По комментарию
```

## Асинхронный клиент (AsyncProxy6)

### Использование с контекстным менеджером
```python
import asyncio
from proxy6_client import AsyncProxy6

async def manage_proxies():
    async with AsyncProxy6(api="ваш_api_ключ") as client:
        # Все операции внутри async with
        info = await client.info()
        print(f"Баланс: {info['balance']} руб.")
        
        # Массовые операции
        if info['balance'] > 100:
            proxies = await client.buy(
                count=5,
                period=15,
                country="de",
                version=4,
                type="socks"
            )
```

### Без контекстного менеджера
```python
async def manual_session():
    client = AsyncProxy6(api="ваш_api_ключ")
    try:
        # Инициализация сессии вручную
        await client.__aenter__()
        
        countries = await client.get_country(version=6)
        print(f"Страны с IPv6: {countries}")
    finally:
        # Закрытие сессии вручную
        await client.close()
```

## 🔧 Основные методы

### 📊 Информационные методы

| Метод | Параметры | Возвращает | Описание |
|-------|-----------|------------|----------|
| `info()` | - | `dict` | Информация об аккаунте |
| `get_price()` | `count`, `period`, `version=6` | `int/float` | Стоимость покупки |
| `get_count()` | `country`, `version=6` | `int` | Количество доступных прокси |
| `get_country()` | `version=6` | `list[str]` | Список доступных стран |
| `get_proxy()` | `state='all'`, `descr=None`, `page=1`, `limit=1000` | `dict` | Список прокси пользователя |
| `check()` | `ids` или `proxy` | `bool` | Проверка валидности прокси |

### 🛒 Методы покупки и управления

| Метод | Параметры | Возвращает | Описание |
|-------|-----------|------------|----------|
| `buy()` | `count`, `period`, `country`, `version=6`, `type='http'`, `descr=None`, `auto_prolong=False` | `dict` | Покупка прокси |
| `prolong()` | `period`, `ids` | `bool` | Продление прокси |
| `delete()` | `ids` или `descr` | `bool` | Удаление прокси |
| `set_type()` | `ids`, `type` | `bool` | Изменение типа протокола |
| `set_descr()` | `new`, `old=None`, `ids=None` | `tuple[bool, int]` | Обновление комментария |


## 📄 Лицензия

```
Proxy6 API Client
Copyright (c) 2026 Alexsey Novikov
```
Распространяется под лицензией MIT.
Подробнее см. в файле [`LICENSE`](LICENSE) или на https://opensource.org/licenses/MIT.


---
<div align="center">

**Разработано с ❤️ [V1vaak](https://github.com/V1vaak)**

[📧 Telegram](https://t.me/novikovyo) | [💻 GitHub](https://github.com/V1vaak) | [🚀 Другие проекты](https://github.com/V1vaak?tab=repositories)

</div>
