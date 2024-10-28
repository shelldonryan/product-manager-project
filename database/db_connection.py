import psycopg

def db_connection():
    try:
        db = psycopg.connect("dbname=product-manager-project user=postgres password=Ryan2018@ host=localhost port=5432")
        return db
    except psycopg.Error as error:
        print(f"Erro ao conectar ao banco de dados: {str(error)}")
        return None

def insert_user(connection, id, username, password, typeUser):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "INSERT INTO users (id, username, password, type) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (id, username, password, typeUser))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro ao registrar usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()

def insert_product(connection, idProduct, nameProduct, quantity, price, userId):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "INSERT INTO product (id, name, quantity, price, userid) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql, (idProduct, nameProduct, quantity, price, userId))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro ao registrar produto: {str(error)}")
        finally:
            cur.close()
            connection.close()

def get_user(connection, username):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            cur.execute(sql, (username,))
            recset = cur.fetchone()
            return recset if recset else False
        except psycopg.Error as error:
            print(f"Erro ao buscar usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()

def get_all_products(connection, userId):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "SELECT * FROM product WHERE userid = %s"
            cur.execute(sql, (userId,))
            recset = cur.fetchall()
            return recset if recset else False
        except psycopg.Error as error:
            print(f"Erro ao buscar produtos para este usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()
