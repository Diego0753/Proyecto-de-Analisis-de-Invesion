from sqlalchemy import create_engine
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

# Función para obtener datos usando SQLAlchemy
def get_data(query):
    engine = create_engine("postgresql+psycopg2://postgres:diego2123@localhost:5432/prueba_tecnica")
    df = pd.read_sql(query, engine)
    return df

# Leer consulta desde el archivo SQL
with open(r'C:\Users\USUARIO\Documents\Diego Universidad\data_postgre\portafolio_banca.sql', 'r', encoding='utf-8') as file:
    query = file.read()

# Inicializar la aplicación Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Análisis de Portafolio por Banca"),
    dcc.Graph(id='grafico-banca'),
    dcc.Dropdown(
        id='dropdown-banca',
        options=[{'label': str(i), 'value': i} for i in get_data("SELECT DISTINCT banca FROM catalogo_banca").banca],
        value=None,
        placeholder="Selecciona una banca"
    )
])

@app.callback(
    Output('grafico-banca', 'figure'),
    Input('dropdown-banca', 'value')
)
def update_graph(selected_banca):
    # Verifica si se ha seleccionado una banca
    if selected_banca is None:
        df = get_data(query)  # Ejecutar la consulta para todas las bancas
    else:
        # Modifica la consulta para filtrar correctamente y preservar la lógica de la consulta original
        filtered_query = f"""
        SELECT 
            b.banca,
            h.macroactivo,
            SUM(CAST(h.aba AS numeric)) AS total_aba,
            (SUM(CAST(h.aba AS numeric)) / SUM(SUM(CAST(h.aba AS numeric))) OVER (PARTITION BY h.cod_banca)) * 100 AS porcentaje_macroactivo
        FROM 
            historico_aba_macroactivos h
        JOIN 
            catalogo_banca b ON h.cod_banca = b.cod_banca
        WHERE 
            h.ingestion_year >= (SELECT MIN(ingestion_year) FROM historico_aba_macroactivos) AND
            h.ingestion_year <= (SELECT MAX(ingestion_year) FROM historico_aba_macroactivos)
        AND 
            b.banca = '{selected_banca}'  -- Filtra por banca seleccionada
        GROUP BY 
            b.banca, h.macroactivo, h.cod_banca;
        """
        df = get_data(filtered_query)  # Ejecutar la consulta filtrada por banca

    # Verifica si df está vacío
    if df.empty:
        return go.Figure()  # Retorna un gráfico vacío o manejador de errores

    # Crear la figura
    fig = go.Figure()

    # Agrupar los datos por macroactivo y banca
    grouped_df = df.groupby(['banca', 'macroactivo']).agg({'porcentaje_macroactivo': 'sum'}).reset_index()

    # Añadir barras para cada macroactivo
    for macroactivo in grouped_df['macroactivo'].unique():
        macro_df = grouped_df[grouped_df['macroactivo'] == macroactivo]
        fig.add_trace(go.Bar(
            x=macro_df['banca'],
            y=macro_df['porcentaje_macroactivo'],
            name=macroactivo
        ))

    # Configurar el diseño
    fig.update_layout(
        title='Porcentaje de Macroactivos por Banca',
        xaxis_title='Banca',
        yaxis_title='Porcentaje del Macroactivo',
        barmode='group',  # Agrupar barras por banca
        yaxis=dict(range=[0, 100])  # Establecer el rango del eje Y entre 0 y 100
    )

    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
