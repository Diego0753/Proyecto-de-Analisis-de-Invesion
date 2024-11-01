from sqlalchemy import create_engine
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


# Función para obtener datos usando SQLAlchemy
def get_data(query):
    engine = create_engine("postgresql+psycopg2://postgres:diego2123@localhost:5432/prueba_tecnica")
    df = pd.read_sql(query, engine)
    return df


# Leer consulta desde el archivo SQL
with open(r'C:\Users\USUARIO\Documents\Diego Universidad\data_postgre\portafolio_evolucion_aba.sql', 'r',
          encoding='utf-8') as file:
    query = file.read()

# Inicializar la aplicación Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Evolución Mensual de ABA Promedio"),
    dcc.Graph(id='grafico-evolucion-aba'),
    # Agregar un componente oculto para forzar la actualización del gráfico
    dcc.Store(id='store', data='initial')
])


@app.callback(
    Output('grafico-evolucion-aba', 'figure'),
    Input('store', 'data')  # Usar un Input ficticio
)
def update_graph(_):
    df = get_data(query)  # Ejecutar la consulta para obtener los datos

    # Imprimir los datos obtenidos para depurar
    print(df)  # Añade esta línea para verificar los datos

    # Verifica si df está vacío
    if df.empty:
        print("No hay datos para graficar.")
        return px.line()  # Retorna un gráfico vacío o manejador de errores

    # Aquí debes asegurarte de que las columnas coincidan con tu consulta
    if 'mes' not in df.columns or 'promedio_aba' not in df.columns:
        print("Las columnas esperadas no están en el DataFrame.")
        print("Columnas disponibles:", df.columns)
        return px.line()  # Retorna un gráfico vacío o manejador de errores

    # Crear gráfico de línea
    fig = px.line(df, x='mes', y='promedio_aba',
                  title='Evolución Mensual de ABA Promedio',
                  labels={'mes': 'Mes', 'promedio_aba': 'Promedio ABA'})

    # Configurar el formato del eje Y
    fig.update_yaxes(title_text='Promedio ABA')

    return fig


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
