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
with open(r'C:\Users\USUARIO\Documents\Diego Universidad\data_postgre\portafolio_perfil_riesgo.sql', 'r',
          encoding='utf-8') as file:
    query = file.read()

# Inicializar la aplicación Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Análisis de Perfil de Riesgo"),
    dcc.Graph(id='grafico-perfil-riesgo'),
    dcc.Dropdown(
        id='dropdown-perfil',
        options=[{'label': str(i), 'value': i} for i in
                 get_data("SELECT DISTINCT perfil_riesgo FROM cat_perfil_riesgo").perfil_riesgo],
        value=None,
        placeholder="Selecciona un perfil de riesgo"
    )
])

@app.callback(
    Output('grafico-perfil-riesgo', 'figure'),
    Input('dropdown-perfil', 'value')
)
def update_graph(selected_perfil):
    # Si no hay perfil seleccionado, ejecutar la consulta original
    if selected_perfil is None:
        df = get_data(query)  # Ejecutar la consulta para todos los perfiles de riesgo
    else:
        # Modificar la consulta para filtrar correctamente por perfil de riesgo
        filtered_query = f"""
        SELECT p.perfil_riesgo, 
               h.macroactivo, 
               SUM(CAST(h.aba AS numeric)) AS total_aba,
               ROUND((SUM(CAST(h.aba AS numeric)) / 
                      SUM(SUM(CAST(h.aba AS numeric))) OVER (PARTITION BY h.cod_perfil_riesgo)) * 100, 2) AS porcentaje_macroactivo
        FROM historico_aba_macroactivos h
        JOIN cat_perfil_riesgo p ON h.cod_perfil_riesgo = p.cod_perfil_riesgo
        WHERE h.ingestion_year >= (SELECT MIN(ingestion_year) FROM historico_aba_macroactivos) 
          AND h.ingestion_year <= (SELECT MAX(ingestion_year) FROM historico_aba_macroactivos)
          AND p.perfil_riesgo = '{selected_perfil}'  -- Filtrar por perfil de riesgo
        GROUP BY p.perfil_riesgo, h.macroactivo, h.cod_perfil_riesgo
        """
        df = get_data(filtered_query)  # Ejecutar la consulta filtrada por perfil de riesgo

    # Verifica si df está vacío
    if df.empty:
        return go.Figure()  # Retorna un gráfico vacío o manejador de errores

    # Crear la figura
    fig = go.Figure()

    # Generar colores únicos para cada macroactivo
    unique_macroactivos = df['macroactivo'].unique()
    colors = {macroactivo: f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)' for macroactivo in unique_macroactivos}

    # Añadir barras para cada macroactivo con su porcentaje
    for macroactivo in unique_macroactivos:
        df_macroactivo = df[df['macroactivo'] == macroactivo]
        fig.add_trace(go.Bar(
            x=df_macroactivo['perfil_riesgo'],
            y=df_macroactivo['porcentaje_macroactivo'],
            name=macroactivo,
            marker_color=colors[macroactivo]  # Asignar un color único por macroactivo
        ))

    # Configurar el diseño
    fig.update_layout(
        title='Porcentaje de Macroactivos por Perfil de Riesgo',
        xaxis_title='Perfil de Riesgo',
        yaxis_title='Porcentaje del Macroactivo',
        yaxis=dict(range=[0, 100]),  # Establecer el rango del eje Y entre 0 y 100
        barmode='group'  # Agrupar barras
    )

    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
