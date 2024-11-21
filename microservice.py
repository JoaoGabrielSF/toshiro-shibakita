from flask import Flask, jsonify
import mysql.connector
import random
import socket
import os

app = Flask(__name__)


DB_CONFIG = {
    'host': '54.234.153.24',
    'user': 'root',
    'password': '5444',
    'database': 'DataStorage'
}


def generate_random_values():
    valor_rand1 = random.randint(1, 999)
    valor_rand2 = os.urandom(4).hex().upper()  
    host_name = socket.gethostname() 
    idade = random.randint(18, 40) 
    matriculado = random.choice([0, 1])  
    return valor_rand1, valor_rand2, host_name, idade, matriculado

def insert_data(valor_rand1, valor_rand2, host_name, idade, matriculado):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = """INSERT INTO dados (AlunoID, Nome, Sobrenome, Endereco, Cidade, Host, Idade, Matriculado)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (valor_rand1, valor_rand2, valor_rand2, valor_rand2, valor_rand2, host_name, idade, matriculado)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return True, "New record created successfully"
    except mysql.connector.Error as err:
        return False, f"Error: {err}"

@app.route('/')
def index():
    valor_rand1, valor_rand2, host_name, idade, matriculado = generate_random_values()
    success, message = insert_data(valor_rand1, valor_rand2, host_name, idade, matriculado)
    
    if success:
        return jsonify({
            "message": message,
            "AlunoID": valor_rand1,
            "Host": host_name,
            "Idade": idade,
            "Matriculado": matriculado
        }), 200
    else:
        return jsonify({"message": message}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
