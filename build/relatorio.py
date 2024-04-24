import streamlit as st 
import mysql.connector
from datetime import datetime
import pandas as pd 


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
    
def selecionardata( data_inicial):
    conn = conectar_mysql()
    cursor = conn.cursor()
    cursor.execute(f"CALL BuscarNotasPorData('{data_inicial}');")
    resultado=cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(resultado, columns=[desc[0] for desc in cursor.description])
    df.drop(columns=['ID'], inplace=True)
    df.rename(columns={'DATA_NOTA':'Dia e hora da avaliação'},inplace=True)
    df.rename(columns={'NOTA':'Avaliação'},inplace=True)
   
    return df



    

def main():
    st.title('Relatório de Avaliação:')
    
    data_minima = datetime(2024, 4, 22)
    data_maxima = datetime.now()
    
    data_inicial = st.date_input("Selecione o dia:", min_value=data_minima, max_value=data_maxima)
    df = selecionardata(data_inicial)

    if df.empty:
        st.warning("A nota para esse dia ainda não está disponível.")
    else:
        filtrar_produto = st.selectbox('Nota:', ['TODOS'] + list(df['Nota'].unique()))
        df_filtrado = df[df['Nota'] == filtrar_produto] if filtrar_produto != 'TODOS' else df
        soma_entrada = df_filtrado['Nota'].count()
        media = df['Nota'].mode()
        valor_media = str(media.iloc[0]) if not media.empty else "N/A"
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f'Quantidade de notas {filtrar_produto}', value=soma_entrada)
        with col2:
            st.metric(label='Média do dia', value=valor_media)

if __name__=="__main__":
    main()