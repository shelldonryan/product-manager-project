import threading
import os
import database as db
from datetime import datetime

def generate_report(user_id):
    report_folder = 'reports'
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    connection = db.db_connection()
    if connection is None:
        print("Erro ao conectar ao banco de dados para gerar o relatório.")
        return
    
    try:
        data = db.get_all_products(connection, user_id)
        products = []

        if data:
            for i in data:
                product = {
                    "name": i[1],
                    "quantity": i[2],
                    "price": str(i[3]),
                }
                products.append(product)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'reports/product_report_{timestamp}.txt'

        with open(filename, 'w') as report_file:
            report_file.write("Products report:\n")
            for product in products:
                report_file.write(f"Produto -> {product['name']}, Quantidade -> {product['quantity']}, Preço -> {product['price']}\n")
        
        print(f"Relatório gerado: {filename}")

    except Exception as e:
        print(f"Erro ao gerar o relatório: {str(e)}")
    
    finally:
        connection.close()

def thread_generate_report(user_id):
    thread = threading.Thread(target=generate_report, args=(user_id,))
    thread.daemon = True
    thread.start()
