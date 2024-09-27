import psycopg

def db_connection():
    try:
        db = psycopg.connect("dbname=product-manager-project user=postgres password=Ryan2018@ host=localhost port=5432")
        return db
    except psycopg.Error as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None

def insert_user(connection, id, username, password, typeUser):
    cur = connection.cursor()

    if connection is not None:
        try:
            sql = "INSERT INTO users (id, username, password, type) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (id, username, password, typeUser))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro to register user: {error.pgconn}")
        finally:
            cur.close()
            connection.close()

def insert_product(connection, idProduct, nameProduct, quantity, price, userId):
    cur = connection.cursor()

    if connection is not None:
        try:
            sql = "INSERT INTO product (id, name, quantity, price, userid) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql, (idProduct, nameProduct, quantity, price, userId))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro to register product: {error.pgconn}")
        finally:
            cur.close()
            connection.close()

def get_user(connection, username, password):
    cur = connection.cursor()

    if connection is not None:
        try:
            cur.execute(f"select * from users where username='{username}' and password='{password}'")
            recset = cur.fetchall()
            connection.close()
            
            if recset:
                return recset[0][0]
            
            return False
        except psycopg.Error as error:
            print(f"Erro to get user: {error.pgconn}")

def get_all_products(connection, userId):
    cur = connection.cursor()
    if connection != None:
        try:
            cur.execute(f"select * from product where userid='{userId}'")
            recset = cur.fetchall()
            connection.close()
            if recset:
                return recset
            
            return False
        except psycopg.Error as error:
            print(f"Erro to get products for this user: {error.pgconn}")
    