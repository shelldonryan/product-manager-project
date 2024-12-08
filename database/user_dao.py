import psycopg

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

def get_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    print(data)

    connection.commit()
    cursor.close()
    connection.close()

    return data

def update_user(connection, id, username, password, typeUser):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "UPDATE users SET username=%s, password=%s, type=%s WHERE id=%s"
            cur.execute(sql, (username, password, typeUser, id))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro ao atualizar usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()

def delete_user(connection, id):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "DELETE FROM users WHERE id=%s"
            cur.execute(sql, (id,))
            connection.commit()
        except psycopg.Error as error:
            print(f"Erro ao deletar usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()