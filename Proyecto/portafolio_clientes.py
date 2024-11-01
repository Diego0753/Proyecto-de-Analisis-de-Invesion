from sqlalchemy import create_engine
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import random


# Función para obtener datos usando SQLAlchemy
def get_data(query):
    engine = create_engine("postgresql+psycopg2://postgres:diego2123@localhost:5432/prueba_tecnica")
    df = pd.read_sql(query, engine)
    return df


# Leer consulta desde el archivo SQL
with open(r'C:\Users\USUARIO\Documents\Diego Universidad\data_postgre\portafolio_cliente1.sql', 'r',
          encoding='utf-8') as file:
    query = file.read()

# Inicializar la aplicación Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Análisis de Portafolio de Clientes"),
    dcc.Graph(id='grafico-portafolio'),
    dcc.Dropdown(
        id='dropdown-cliente',
        options=[{'label': str(i), 'value': i} for i in
                 get_data("SELECT DISTINCT id_sistema_cliente FROM historico_aba_macroactivos").id_sistema_cliente],
        value=None,
        placeholder="Selecciona un cliente"
    )
])


@app.callback(
    Output('grafico-portafolio', 'figure'),
    Input('dropdown-cliente', 'value')
)
def update_graph(selected_cliente):
    if selected_cliente is None:
        df = get_data(query)  # Ejecutar la consulta para todos los clientes
    else:
        # Modifica la consulta para filtrar correctamente
        filtered_query = f"{query} WHERE id_sistema_cliente = '{selected_cliente}';"
        df = get_data(filtered_query)  # Ejecutar la consulta filtrada por cliente

    # Verifica si df está vacío
    if df.empty:
        return go.Figure()  # Retorna un gráfico vacío o manejador de errores

    # Agrupar los datos por macroactivo
    total_macroactivos = df.groupby('macroactivo').agg({'porcentaje_macroactivo': 'sum'}).reset_index()

    # Crear la figura
    fig = go.Figure()

    # Añadir la barra total del macroactivo
    fig.add_trace(go.Bar(
        x=total_macroactivos['macroactivo'],
        y=total_macroactivos['porcentaje_macroactivo'],
        name='Total Macroactivo',
        marker_color='lightblue'
    ))

    # Generar colores aleatorios para cada activo
    colors = [f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)' for _ in
              range(len(df))]

    # Añadir barras para cada activo con colores diferentes
    for index, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['macroactivo']],
            y=[row['porcentaje_activo_macroactivo']],
            name=row['nombre_activo'],
            marker_color=colors[index % len(colors)]  # Asignar un color aleatorio
        ))

    # Configurar el diseño
    fig.update_layout(
        title='Porcentaje de Macroactivos y Activos por Cliente',
        xaxis_title='Macroactivos',
        yaxis_title='Porcentaje del Macroactivo',
        yaxis=dict(range=[0, 100]),  # Establecer el rango del eje Y entre 0 y 100
        barmode='group'  # Agrupar barras
    )

    return fig


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
