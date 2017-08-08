from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1',
                             db='Store',
                             charset='utf8mb4',
                             autocommit=True,
                             cursorclass= pymysql.cursors.DictCursor)
cursor = connection.cursor()


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@get('/categories')
def list_Categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, name from categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps ({"STATUS": "SUCCESS", "CATEGORIES": result, "CODE":"200"})

    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})

@get('/products')
def list_Products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE": "200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})

@get('/category/<id>/products')
def get_Products(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products WHERE category = {} order by favorite desc".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "PRODUCTS": result, "CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})


@get ("/product/<id>")
def get_the_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from products where id = {}".format(id)
            cursor.execute(sql)
            result = cursor.fetchone()
            return json.dumps({"STATUS": "SUCCESS", "MSG":result,"CODE":"200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})


@post ("/category")
def create_category():
    try:
        with connection.cursor() as cursor:
            name = request.POST.get("name")
            sql = "INSERT INTO categories VALUES (0,'{}')".format(name)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": result, "CODE": "200"})
    except:
        return json.dumps({"STATUS": "INTERNAL ERROR", "MSG": "There was an internal error", "CODE": "500"})


@delete("/category/<id>")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE id = {}".format(id)
            cursor.execute(sql)
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The category was deleted successfully", "CODE": "200"})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "The category was not deleted due to an error", "CODE": "500"})


@delete("/product/<id>")
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products where id = {}".format(id)
            cursor.execute(sql)
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was deleted successfully", "CODE": "200"})
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "The product was not deleted due to an error", "CODE": "500"})


#run(host='0.0.0.0', port=argv[1])
run(host='127.0.0.1', port=7000)