# Proxy6 API Client

## Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## Описание
Синхронный и асинхронный клиенты для взаимодействия с API сервиса Proxy6 (https://px6.me/).
### Ссылки
- [Официальный сайт Proxy6](https://px6.me/)
- [Официальная документация Proxy6 API](https://px6.me/ru/developers)
- [Получение API ключа](https://px6.me/ru/user/developers)

## Установка

```bash
# Клонировать репозиторий
git clone https://github.com/V1vaak/PROXY6_TOOLS
cd PROXY6_TOOLS

# Установка нужных библиотек
pip install requests aiohttp
```

## Синхронный клиент

```python
from proxy6_client import Proxy6

# Инициализация клиента
client = Proxy6(api="ваш_api_ключ")

try:
    # Получение списка стран
    countries = client.get_country()
    print(f"Доступные страны: {countries}")
    
    # Получение цены
    price = client.get_price(count=10, period=30, version=4)
    print(f"Стоимость 10 IPv4 прокси на 30 дней: {price} руб.")
    
    # Покупка прокси
    proxies = client.buy(
        count=5,
        period=15,
        country="ru",
        version=4,
        type="socks",
        descr="Мои рабочие прокси"
    )
    print(f"Куплены прокси: {proxies}")
    
finally:
    # Закрытие сессии
    client.close()
```

## Асинхронный клиент

```python
import asyncio
from proxy6_client import AsyncProxy6

async def main():
    async with AsyncProxy6(api="ваш_api_ключ") as client:
        # Получение информации о балансе
        info = await client.info()
        print(f"Баланс: {info.get('balance')} руб.")
        
        # Получение списка прокси
        proxies = await client.get_proxy(state="active")
        print(f"Активные прокси: {len(proxies)}")
        
        # Проверка прокси
        if proxies:
            proxy_id = list(proxies.keys())[0]
            is_valid = await client.check(ids=proxy_id)
            print(f"Прокси {proxy_id} валиден: {is_valid}")

# Запуск
asyncio.run(main())
```

## Основные методы

### Управление прокси

#### Получение информации
```python
# Синхронно
proxies = client.get_proxy(state="active", limit=100)
countries = client.get_country(version=4)
available_count = client.get_count(country="us", version=6)

# Асинхронно
proxies = await client.get_proxy(state="expiring")
info = await client.info()
```

#### Покупка прокси
```python
# IPv4 HTTP прокси
proxies = client.buy(
    count=10,
    period=30,
    country="de",
    version=4,
    type="http",
    descr="Немецкие прокси",
    auto_prolong=True
)

# IPv6 SOCKS5 прокси
proxies = await client.buy(
    count=5,
    period=7,
    country="us",
    version=6,
    type="socks",
    descr="Американские SOCKS5"
)
```

#### Управление прокси
```python
# Изменение типа протокола
client.set_type(ids=(12345, 12346), type="socks")

# Обновление комментария
success, count = client.set_descr(
    new="Обновленный комментарий",
    ids=(12345, 12346)
)

# Продление
client.prolong(period=30, ids=(12345, 12346))

# Удаление
client.delete(ids=12345)
# или по комментарию
client.delete(descr="Устаревшие прокси")
```

### Информационные методы

```python
# Расчет стоимости
price = client.get_price(count=100, period=365, version=4)
print(f"Стоимость: {price} руб.")

# Проверка доступности
available = client.get_count(country="ru", version=4)
print(f"Доступно в России: {available} IPv4 прокси")

# Проверка валидности
is_valid = client.check(proxy="1.2.3.4:8080:user:pass")
# или
is_valid = client.check(ids=12345)
```

## Обработка ошибок

```python
from proxy6_client import Proxy6, Proxy6Error

client = Proxy6(api="ваш_api_ключ")

try:
    result = client.buy(count=1000, period=1, country="xx")
except Proxy6Error as e:
    print(f"Ошибка API: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")
finally:
    client.close()
```

## Параметры методов

### Версии прокси
- `version=4` - IPv4 выделенные прокси
- `version=3` - IPv4 Shared (общие)
- `version=6` - IPv6 прокси (по умолчанию)

### Типы протоколов
- `type="http"` - HTTP/HTTPS прокси
- `type="socks"` - SOCKS5 прокси

### Статусы прокси
- `state="active"` - активные
- `state="expired"` - истекшие
- `state="expiring"` - заканчивающиеся
- `state="all"` - все (по умолчанию)


## Требования

- Python 3.8+
- requests >= 2.25.0
- aiohttp >= 3.8.0
