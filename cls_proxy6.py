from requests import get


class Proxy6:
    """
    Класс для взаимодействия с API Proxy6. Сайт (https://px6.me/).
    
    Parameters
    ----------
    api : str
        API-ключ для аутентификации в сервисе Proxy6.
    """
    
    def __init__(self, api: str):
        self.api = api

    def __get_url(self, method_name: str, **params) -> str:
        '''
        Функция возвращает готовую ссылку для get запроса 
        с учетом метода и его параметров.

        Notes
        -----
        Функция для внутреклассового использования (служебная).
        '''
        url = f'https://px6.link/api/{self.api}/{method_name}?'

        cnt = len(params)
        i = 1
        for key in params:
            value = params[key]
            if isinstance(value, tuple):
                value = str(value).replace('(', '').replace(')', '').replace(' ', '')
            url += f'{key}={value}' if cnt == i else f'{key}={value}&'
            i += 1

        return url
    
    def __have_connection(self, data: dict) -> bool[True]:
        """
        Проверяет подключение к API.

        Parameters
        ----------
        data : dict
            Данные ответа API.

        Returns
        -------
        True, если есть успешное подключение.

        Raises
        ------
        Exception
            Если не удалось подключиться (статус 'no').
        
        Notes
        -----
        Функция для внутреклассового использования (служебная).

        """     
        if data['status'] == 'yes':
            return True
        raise Exception('NoConection')
    
    def getprice(self, *, count: int, period: int, version: int = 6) -> int | float:
        """
        Получает стоимость покупки прокси.

        Parameters
        ----------
        count : int
            Количество прокси (обязательный параметр).
        period : int
            Период в днях (обязательный параметр).
        version : int, optional
            Версия прокси: <b>4</b> - IPv4, <b>3</b> - IPv4 Shared, <b>6</b> - IPv6 (по умолчанию 6).

        Returns
        -------
        int or float
            Стоимость прокси в <b>рублях</b> (ru, RUB).
        """
        url = self.__get_url(self.getprice.__name__, count=count, period=period, version=version)
        data = get(url).json()

        if self.__have_connection(data):
            return data['price']
    
    def getcount(self, *, country: str, version: int = 6) -> int:
        """
        Получает количество доступных прокси для определенной страны.

        Parameters
        ----------
        country : str
            Код страны в формате ISO2 (обязательный параметр).
        version : int, optional
            Версия прокси: <b>4</b> - IPv4, <b>3</b> - IPv4 Shared, <b>6</b> - IPv6 (по умолчанию 6).

        Returns
        -------
        int
            Количество доступных прокси.
        """
        url = self.__get_url(self.getcount.__name__, country=country, version=version)
        data = get(url).json()

        if self.__have_connection(data):
            return data['count']
    
    def getcountry(self, *, version: int = 6) -> list:
        """
        Получает все страны, прокси которых можно приобрести.

        Parameters
        ----------
        version : int, optional
            Версия прокси: <b>4</b> - IPv4, <b>3</b> - IPv4 Shared, <b>6</b> - IPv6 (по умолчанию 6).

        Returns
        -------
        list[str, ..., str]
            Список доступных стран.
        """
        url = self.__get_url(self.getcountry.__name__, version=version)
        data = get(url).json()

        if self.__have_connection(data):
            return data['list']
    
    def getproxy(self, *, state: str = 'all', descr: str = None, 
                page: int = 1, limit: int = 1000) -> dict:
        """
        Получает информацию о прокси объекта класса Proxy6.

        Parameters
        ----------
        state : str, optional
            Состояние прокси: 'active' - активные, 'expired' - неактивные, 
            'expiring' - заканчивающиеся, 'all' - все (по умолчанию 'all').
        descr : str, optional
            Технический комментарий, указанный при покупке прокси.
        page : int, optional
            Номер страницы для пагинации (по умолчанию 1).
        limit : int, optional
            Количество прокси для вывода (по умолчанию 1000, максимальное).

        Returns
        -------
        dict
            Информация о прокси.
        """
        if descr:       
            url = self.__get_url(self.getproxy.__name__, state=state, descr=descr, page=page, limit=limit)
        else:
            url = self.__get_url(self.getproxy.__name__, state=state, page=page, limit=limit)
        
        data = get(url).json()

        if self.__have_connection(data):
            return data['list']
        
    def settype(self, *, ids: tuple, type: str) -> bool[True]:
        """
        Изменяет тип (протокол) ваших прокси.

        Parameters
        ----------
        ids : tuple
            Внутренние номера прокси в системе, кортежем (обязательный параметр).
        type : str
            Устанавливаемый тип: 'http' - HTTPS, или 'socks' - SOCKS5 (обязательный параметр).

        Returns
        -------
        True, если успешно.
        """
        url = self.__get_url(self.settype.__name__, ids=ids, type=type)
        data = get(url).json()

        if self.__have_connection(data):
            return True

    def setdescr(self, *, new: str, old: str = None, ids: tuple = None) -> tuple:
        """
        Обновляет технический комментарий у ваших прокси.

        Parameters
        ----------
        new : str
            Новый технический комментарий, макс. 50 символов (обязательный параметр).
        old : str, optional
            Старый технический комментарий для изменения.
        ids : tuple, optional
            Внутренние номера прокси в системе.

        Returns
        -------
        tuple
            (True, count), если успешно. count - число обновленных прокси.

        Notes
        -----
        Обязательно должен присутствовать один из параметров: либо 'ids', либо 'old'.
        """
        if old and not ids:
            url = self.__get_url(self.setdescr.__name__, new=new, old=old)
        elif ids and not old:
            url = self.__get_url(self.setdescr.__name__, new=new, ids=ids)
        
        data = get(url).json()

        if self.__have_connection(data):
            return True, data['count']
                
    def buy(self, *, count: int, period: int, country: str, version: int = 6, 
            type: str = 'http', descr: str = None, auto_prolong: bool = False) -> dict:
        """
        Покупает прокси.

        Parameters
        ----------
        count : int
            Количество прокси для покупки (обязательный параметр).
        period : int
            Период в днях (обязательный параметр).
        country : str
            Код страны в формате ISO2 (обязательный параметр).
        version : int, optional
            Версия прокси: <b>4</b> - IPv4, <b>3</b> - IPv4 Shared, <b>6</b> - IPv6 (по умолчанию 6).
        type : str, optional
            Тип прокси: 'socks' или 'http' (по умолчанию 'http').
        descr : str, optional
            Технический комментарий для списка прокси, макс. 50 символов.
        auto_prolong : bool, optional
            Включить автопродление для купленных прокси.

        Returns
        -------
        dict
            Список купленных прокси.
        """
        if descr and auto_prolong:
            url = self.__get_url(self.buy.__name__, count=count, 
                                 period=period, country=country, 
                                 version=version, type=type, 
                                 descr=descr, auto_prolong=auto_prolong)
        elif descr:
            url = self.__get_url(self.buy.__name__, count=count, 
                                 period=period, country=country, 
                                 version=version, type=type, 
                                 descr=descr)
        elif auto_prolong:
            url = self.__get_url(self.buy.__name__, count=count, 
                                 period=period, country=country, 
                                 version=version, type=type, 
                                 auto_prolong=auto_prolong)
        else:
            url = self.__get_url(self.buy.__name__, count=count, period=period, country=country, version=version, type=type)

        data = get(url).json()

        if self.__have_connection(data):
            return data['list']
        
    def prolong(self, *, period: int, ids: int | tuple) -> bool:
        """
        Продлевает текущие прокси.

        Parameters
        ----------
        period : int
            Период продления в днях (обязательный параметр).
        ids : int or tuple
            Внутренние номера прокси в системе (обязательный параметр).

        Returns
        -------
        True, если успешно.
        """
        url = self.__get_url(self.prolong.__name__, period=period, ids=ids)
        data = get(url).json()
        
        if self.__have_connection(data):
            return True
        
    def delete(self, *, ids: int = None, descr: str = None) -> bool:
        """
        Удаляет прокси.

        Parameters
        ----------
        ids : int, optional
            Внутренние номера прокси в системе.
        descr : str, optional
            Технический комментарий, указанный при покупке прокси.

        Returns
        -------
        True, если успешно.

        Notes
        -----
        Обязательно должен присутствовать один из параметров: либо 'ids', либо 'descr'.
        """
        if ids and descr:
            url = self.__get_url(self.delete.__name__, ids=ids, descr=descr)
        elif ids:
            url = self.__get_url(self.delete.__name__, ids=ids)
        else:
            url = self.__get_url(self.delete.__name__, descr=descr)

        data = get(url).json()

        if self.__have_connection(data):
            return True
        
    def check(self, *, ids: int = None, proxy: str = None) -> bool:
        """
        Проверяет валидность прокси.

        Parameters
        ----------
        ids : int, optional
            Внутренний номер прокси в системе (обязательный если не указан proxy).
        proxy : str, optional
            Строка прокси в формате: ip:port:user:pass (обязательный если не указан ids).

        Returns
        -------
        bool
            True если прокси валиден, False в противном случае.
        """
        if ids:
            url = self.__get_url(self.check.__name__, ids=ids)
        elif proxy:
            url = self.__get_url(self.check.__name__, proxy=proxy)
        
        data = get(url).json()

        if self.__have_connection(data):
            return data['proxy_status']

    def __str__(self) -> str:
        """
        Возвращает строковое представление статуса API.

        Returns
        -------
        str
            Информация о статусе API.
        """
        url = f'https://px6.link/api/{self.api}'

        return str(get(url).json())
