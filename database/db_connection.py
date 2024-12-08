import psycopg, os
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    try:
        db = psycopg.connect(f"dbname={os.getenv("NAME_DB")} user={os.getenv("USER_DB")} password={os.getenv("PASSWORD_DB")} host=localhost port=5432")
        return db
    except psycopg.Error as error:
        print(f"Erro ao conectar ao banco de dados: {str(error)}")
        return None