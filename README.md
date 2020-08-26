# WSGI приложение без использования фреймворков
### Приложение выполнено в качестве тестового задания для собеседования.
Задача состояло в том, чтобы написать приложение, которое может работать с любым wsgi сервером и не использовать при этом никаких фреймворков.

В данном приложении используется только одна не cтандартная библиотека **WebOb** для форирования **Request** и **Response**.
### Стек
- Python3
- SQLite
- JavaScript
- Docker

### Запуск
Склонируйте репозиторий
Из каталога с приложением:
``` docker-compose up ```


При запуске приложение создает БД и наполняет его исходными данными.
В качестве веб-сервера в контейнере используется gunicorn
Приложение запускаяется на 8000 порту.
По адресу /comment/ отображаться форма для заполнения:
•	фамилия
•	имя
•	отчество
•	регион
•	город
•	контактный телефон
•	e-mail
•	комментарий.

Поля фамилия, имя и комментарий являются обязательными. Поле комментарий текстовое.
Для полей телефон и email следует производится проверка ввода. 
Поля с некорректным вводом и не заполненные обязательные поля визуально выделяться красным цветом.
Поля регион и город являются выпадающими списками, при этом список выбора поля город зависит от выбранного поля регион. 
Данные для этих списков храниться в БД. Значение в поля город динамически подгружаться по технологии ajax в соответствии с выбранным полем регион.

При обращении по относительному пути /view/ выводиться таблица со списком добавленных комментариев. 
На этой же странице есть возможность удалить определенную запись.

При обращении по относительному пути /stat/ выводиться таблица со списком тех регионов, у которых количество комментариев больше 5, 
выводит также и количество комментариев по каждому региону. Каждая строчка - ссылка на список городов этого региона, 
в котором отображается количество комментариев по этому городу.
