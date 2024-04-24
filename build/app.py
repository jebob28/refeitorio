from flask import Flask ,render_template,request,jsonify
import mysql.connector
from datetime import datetime

 
app=Flask(__name__)
def conectar_mysql():
    config = {
        'user': 'root',
        'password': 'kali',
        'host': '192.168.1.190',
        'port': '32768',
        'database': 'AvaliacaoRefeitorio',
        'raise_on_warnings': True
    }
    try:
        # Conectando ao banco de dados
        conn = mysql.connector.connect(**config)

        if conn.is_connected():
            return conn
        else:
            print('Falha ao conectar.')
            return None

    except mysql.connector.Error as e:
        print(f'Erro ao conectar ao MySQL: {e}')
        return None
def inserir_nota(nota):
    conn = conectar_mysql()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Obtendo a data e hora atual
            data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Executando a consulta de inserção
            cursor.execute("INSERT INTO Nota (NOTA, DATA_NOTA) VALUES (%s, %s)", (nota, data_hora))
            # Commit para aplicar as alterações
            conn.commit()
            print("Avaliação registrada com sucesso.")
        except mysql.connector.Error as e:
            print(f'Erro ao registrar a avaliação no MySQL: {e}')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if conn.is_connected():
                conn.close()
                
@app.route('/vote', methods=['POST'])
def vote():
    nota = request.form.get('nota')
    response = inserir_nota(nota)
    return jsonify({'message': response})
@app.route('/',methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)