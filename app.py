from api import APP
from db import DBconnect
import json
 
app = APP()
conn = DBconnect()
cursor = conn.cursor()

@app.route("/comment/")
def home(request, response):
    """Представление для /comment/."""
    if request.method == 'GET':
        response.body = get_html('comment.html')

    elif request.method == 'POST':
        create_comment(request)
        response.body = get_html('success.html')


def create_comment(request):
    """Добавление нового комментария.
       Данные для полей таблицы получаем из параметров POST запроса.
       Формируем SQL запрос и исполняем его.
    """
    last_name = request.POST.get('last_name')
    assert last_name != '', 'Фамилия должна быть заполнена'
    first_name = request.POST.get('first_name')
    assert first_name != '', 'Имя должно быть заполнено'
    patronymic = request.POST.get('patronymic')
    region = request.POST.get('region')
    city = request.POST.get('city')
    tel = request.POST.get('tel')
    email = request.POST.get('email')
    comment = request.POST.get('text')
    assert comment != '', 'Комментарий должен быть заполнен'

    sql = '''INSERT INTO comments 
        ('last_name', 'first_name', 'patronymic', 'comment', 'region', 'city', 'tel', 'email')
        VALUES (?,?,?,?,?,?,?,?)'''
    cursor.execute(sql, [last_name, first_name, patronymic, comment, region, city, tel, email])
    conn.commit()


def get_html(html):
    """Функция возвращает шаблон страницы. На вход получает имя html файла"""
    with open('templates/' + html, 'rb') as f:
        return f.read()


@app.route("/view/")
def view(request, response):
    """Представление для /view/."""
    response.body = get_html('view.html')


@app.route("/stat/")
def stat(request, response):
    """Представление для /stat/."""
    response.body = get_html('stat.html')


@app.route("/js")
def send_js(request, response):
    """Отдает JS файл для страницы /comment/"""
    response.body = get_html('main.js')


@app.route("/stat-js")
def send_js(request, response):
    """Отдает JS файл для страницы /stat/"""
    response.body = get_html('stat.js')


@app.route("/view-js")
def send_js(request, response):
    """Отдает JS файл для страницы /view/"""
    response.body = get_html('view.js')


@app.route("/regions")
def regions(request, response):
    """Функция возвращает JSON со списком всех регионов из таблицы region.
       Выполняется запрос к БД, полученные данные сериализуются в JSON формат
       Доступны только POST запосы
    """
    if request.method == 'POST':
        sql = "SELECT region_id, name FROM region"
        cursor.execute(sql)
        regions_list = cursor.fetchall()
        data = {
            'regions': regions_list
        }
        response.text = json.dumps(data, ensure_ascii=False)
        response.content_type ='application/json'

    elif request.method == 'GET':
        response.status_code = 403


@app.route("/citys")
def citys(request, response):
    """Функция получает идентификатор региона, 
       запрашивает все города связанные с данным регионом 
       и отвечает JSONом со списком городов.
    """
    if request.method == 'POST':
        region = request.POST.get('region')
        sql = "SELECT city_id, name FROM city WHERE region = ?"
        cursor.execute(sql, (region,))
        citys_list = cursor.fetchall()
        data = {
            'citys': citys_list
        }
        response.text = json.dumps(data, ensure_ascii=False)
        response.content_type ='application/json'

    elif request.method == 'GET':
        response.status_code = 403


@app.route("/stat-regions")
def stat_regions(request, response):
    if request.method == 'POST':
        """Функция возвращает JSON со списком регионов и 
           колличеством комментариев по каждому региону.
           В результаты попадают только те регионы где более 5 комментариев.
           Отсортированно по убыванию.
        """
        sql = """SELECT region.region_id, region.name, COUNT(comment_id) as count
            FROM comments INNER JOIN region ON region.region_id = region 
            GROUP BY region.region_id, region.name HAVING COUNT(comment_id) > 5 ORDER BY count DESC"""
        cursor.execute(sql)
        regions = cursor.fetchall()
        data = {
            'result': regions
        }
        response.text = json.dumps(data, ensure_ascii=False)
        response.content_type ='application/json'

    elif request.method == 'GET':
        response.status_code = 403


@app.route("/stat-city")
def stat_city(request, response):
    if request.method == 'POST':
        """Формирует список городов полученного региона
           с колличеством комментариев по каждому городу.
           Данные из текущего представления подтягиваются на странице /stat/ при клике на регионе.
        """
        region = request.POST.get('region')
        sql = """SELECT city.city_id, city.name, COUNT(comment_id) as count
            FROM comments INNER JOIN region ON region.region_id = comments.region 
            INNER JOIN city ON city.city_id = comments.city
            WHERE region.region_id = ? GROUP BY city.city_id, city.name ORDER BY count DESC"""
        cursor.execute(sql, (region,))
        citys = cursor.fetchall()
        data = {
            'result': citys
        }
        response.text = json.dumps(data, ensure_ascii=False)
        response.content_type ='application/json'

    elif request.method == 'GET':
        response.status_code = 403


@app.route("/all-comments")
def all_comments(request, response):
    """Все комментарии из таблицы comments для вывода на странице /view/."""
    if request.method == 'POST':
        sql = """SELECT comment_id, first_name, last_name, comment, city.name
            FROM comments LEFT JOIN city ON city.city_id = city"""
        cursor.execute(sql)
        comments = cursor.fetchall()
        data = {
            'result': comments
        }
        response.text = json.dumps(data, ensure_ascii=False)
        response.content_type ='application/json'

    elif request.method == 'GET':
        response.status_code = 403


@app.route("/delete-comment")
def delete_comment(request, response):
    """Функция получает ID комментария и удаляет объект с данным ID из таблицы comments."""
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        sql = """DELETE FROM comments WHERE comment_id = ?"""
        cursor.execute(sql, (comment_id,))
        comment = cursor.fetchall()
        conn.commit()
        data = {
            'result': 'ok'
        }
        response.text = json.dumps(data, ensure_ascii=False)
        response.content_type ='application/json'

    elif request.method == 'GET':
        response.status_code = 403
