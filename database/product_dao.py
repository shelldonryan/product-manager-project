import psycopg

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

def get_product_by_userid(connection, userId):
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM product WHERE userId = %s", (userId,))
    
    data = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()
    return data

def get_product(connection, nameProduct=None, id=None):
    cursor = connection.cursor()
    if id is not None:
        cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
    else:
        cursor.execute("SELECT * FROM product WHERE name = %s", (nameProduct,))
    
    data = cursor.fetchone()
    print(data)

    connection.commit()
    cursor.close()
    connection.close()
    return data

def update_product(connection, id, nameProduct, quantity, price):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "UPDATE product SET name=%s, quantity=%s, price=%s WHERE id=%s"
            cur.execute(sql, (nameProduct, quantity, price, id))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro ao atualizar produto: {str(error)}")
        finally:
            cur.close()
            connection.close()

def delete_product(connection, id):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "DELETE FROM product WHERE id=%s"
            cur.execute(sql, (id,))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro ao deletar produto: {str(error)}")
        finally:
            cur.close()
            connection.close()