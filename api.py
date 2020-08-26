"""Использовал стороннюю библиотеку для формирования запроса и ответа."""
from webob import Request, Response


class APP:
    """Клас основного WSGI приложения.
       В конструкторе класса создаем словарь для формирования доступных маршрутов.
    """
    def __init__(self):
        self.routes = {}
 

    def route(self, path):
        """Декоратор для представлений. В качестве аргумента принимает функцию представления
           с аргументом  - маршрутом. Формирует словарь - маршрут[функция которая его обрабатывает]
        """
        def wrapper(handler):
            self.routes[path] = handler
            return handler
 
        return wrapper


    def __call__(self, environ, start_response):
        """При вызове объекта приложения формирует запос и ответ.
           Ответ формируется на основе request.path.
        """
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)


    def handle_request(self, request):
        """Метод ищет обработчик на соответсвующий request_path.
           Если не находит, возвращает метод default_response
        """
        response = Response()
        handler = self.find_handler(request_path=request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)
 
        return response


    def find_handler(self, request_path):
        """Поиск в словаре routes обработчика для полученного path."""
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    
    def default_response(self, response):
        """Метод возврашает ошибку 404."""
        response.status_code = 404
        response.text = "Not found."

