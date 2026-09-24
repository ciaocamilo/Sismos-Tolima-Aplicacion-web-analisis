# Capa gráfica: definición del layout de la aplicación
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

# Cada 30 minutos se vuelve a consultar el endpoint del SGC (ver logica.py)
INTERVALO_ACTUALIZACION_MS = 30 * 60 * 1000

# Paleta de colores
_AZUL  = '#00184a'
_FONDO = '#F2F3F8'

# Estilo
_CARD = {
    'border': '1px solid #c0c0c0',
    'borderRadius': '8px',
    'overflow': 'hidden',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
    'backgroundColor': 'white',
}


def _panel(child, height):
    # Envuelve un dcc.Graph, Iframe u otro componente en un panel con bordes
    return html.Div(child, className='panel-grafico', style={**_CARD, 'height': height})


def _titulo(texto, icono=None):
    contenido = [html.I(className=f'bi {icono} me-2')] if icono else []
    contenido.append(texto)
    return html.H5(
        contenido,
        style={
            'textAlign': 'center',
            'color': _AZUL,
            'marginBottom': '10px',
            'fontWeight': '600',
        },
    )


layout = html.Div(
    [
        dcc.Interval(id='interval-actualizacion', interval=INTERVALO_ACTUALIZACION_MS, n_intervals=0),

        # Header
        html.Header(
            [
                html.H1(
                    [html.I(className='bi bi-activity me-2'), 'Análisis de Sismos'],
                    style={'textAlign': 'center', 'color': 'white',
                           'margin': '0', 'padding': '22px 0 4px'},
                ),
                html.P(
                    'Monitoreo sismológico del departamento del Tolima',
                    style={'textAlign': 'center', 'color': '#c7d2f0',
                           'margin': '0', 'paddingBottom': '18px', 'fontSize': '0.95rem'},
                ),
            ],
            className='encabezado-sismos',
        ),

        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        html.H2('Departamento del Tolima - Colombia', style={'textAlign': 'center'}),
                        width=12,
                    ),
                    className='mt-4 mb-1',
                ),

                # Introducción
                dbc.Row(
                    dbc.Col(
                        html.P(
                            [
                                'Esta aplicación no oficial consulta en tiempo real el endpoint público del ',
                                html.Strong('Servicio Geológico Colombiano (SGC)'),
                                ' para analizar los sismos registrados con epicentro en el departamento '
                                'del Tolima durante la última semana. La información se actualiza '
                                'automáticamente cada 30 minutos.',
                            ],
                            style={
                                'color': '#444',
                                'fontSize': '0.97rem',
                                'lineHeight': '1.7',
                                'marginTop': '32px',
                                'marginBottom': '16px',
                            },
                        ),
                        width=12,
                    ),
                    className='mb-3',
                ),

                # Banner con rango de fechas y última actualización
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            id='banner-actualizacion',
                            style={
                                'backgroundColor': _FONDO,
                                'border': f'1px solid {_AZUL}',
                                'borderRadius': '6px',
                                'padding': '10px 16px',
                                'color': _AZUL,
                                'fontSize': '0.9rem',
                                'textAlign': 'center',
                            },
                        ),
                        width=12,
                    ),
                    className='mb-4',
                ),

                # Mensaje mostrado cuando no hay sismos en el rango consultado
                dbc.Row(
                    dbc.Col(html.Div(id='mensaje-sin-datos'), width=12),
                    className='mb-2',
                ),

                # Tarjetas KPI (resumen rápido)
                dbc.Row(id='fila-kpis', className='mb-4 g-3'),

                # 1. Mapa satelital (Folium) y 2. Mapa interactivo (Plotly)
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                _titulo('Ubicación de sismos - Vista satelital', 'bi-globe-americas'),
                                _panel(html.Iframe(id='iframe-satelital', style={'width': '100%', 'height': '100%', 'border': 'none'}), '600px'),
                            ],
                            xs=12, lg=6, className='mb-4',
                        ),
                        dbc.Col(
                            [
                                _titulo('Ubicación de sismos - Magnitud y profundidad', 'bi-geo-alt'),
                                _panel(dcc.Graph(id='graph-mapa-plotly', responsive=True, style={'height': '100%'}), '600px'),
                            ],
                            xs=12, lg=6, className='mb-4',
                        ),
                    ],
                ),

                # 3. Serie temporal diaria
                dbc.Row(
                    dbc.Col(
                        [
                            _titulo('Sismos diarios en el Tolima', 'bi-graph-up'),
                            _panel(dcc.Graph(id='graph-serie-diaria', responsive=True, style={'height': '100%'}), '390px'),
                        ],
                        width=12,
                    ),
                    className='mb-4',
                ),

                # 4. Distribución de magnitudes y profundidades
                dbc.Row(
                    dbc.Col(
                        [
                            _titulo('Distribución de magnitudes y profundidades', 'bi-bar-chart-line'),
                            _panel(dcc.Graph(id='graph-distribucion', responsive=True, style={'height': '100%'}), '390px'),
                        ],
                        width=12,
                    ),
                    className='mb-4',
                ),

                # 5. Magnitud vs. profundidad
                dbc.Row(
                    dbc.Col(
                        [
                            _titulo('Magnitud vs. Profundidad', 'bi-graph-up-arrow'),
                            _panel(dcc.Graph(id='graph-mag-profundidad', responsive=True, style={'height': '100%'}), '420px'),
                        ],
                        width=12,
                    ),
                    className='mb-4',
                ),

                # 6. Top ubicaciones con más sismos
                dbc.Row(
                    dbc.Col(
                        [
                            _titulo('Top 15 ubicaciones con más sismos', 'bi-pin-map'),
                            _panel(dcc.Graph(id='graph-top-ubicaciones', responsive=True, style={'height': '100%'}), '440px'),
                        ],
                        width=12,
                    ),
                    className='mb-4',
                ),

                # 7. Patrón horario
                dbc.Row(
                    dbc.Col(
                        [
                            _titulo('Sismos por hora del día (hora local)', 'bi-clock-history'),
                            _panel(dcc.Graph(id='graph-patron-horario', responsive=True, style={'height': '100%'}), '390px'),
                        ],
                        width=12,
                    ),
                    className='mb-4',
                ),

                # 8. Mapa de calor de densidad y 9. Clustering espacial
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                _titulo('Mapa de calor de densidad de sismos', 'bi-fire'),
                                _panel(html.Iframe(id='iframe-calor', style={'width': '100%', 'height': '100%', 'border': 'none'}), '600px'),
                            ],
                            xs=12, lg=6, className='mb-4',
                        ),
                        dbc.Col(
                            [
                                _titulo('Clusters espaciales de sismos (KMeans)', 'bi-diagram-3'),
                                _panel(dcc.Graph(id='graph-clusters', responsive=True, style={'height': '100%'}), '600px'),
                            ],
                            xs=12, lg=6, className='mb-4',
                        ),
                    ],
                ),

                # 10. Tabla detallada de sismos filtrados (Tolima)
                dbc.Row(
                    dbc.Col(
                        [
                            _titulo('Registro detallado de sismos en el Tolima', 'bi-table'),
                            html.Div(
                                dash_table.DataTable(
                                    id='tabla-sismos',
                                    columns=[
                                        {'name': 'Fecha', 'id': 'Fecha'},
                                        {'name': 'Hora local', 'id': 'Hora'},
                                        {'name': 'Ubicación', 'id': 'Ubicacion'},
                                        {'name': 'Magnitud', 'id': 'Magnitud'},
                                        {'name': 'Profundidad (km)', 'id': 'Profundidad'},
                                    ],
                                    page_size=12,
                                    sort_action='native',
                                    filter_action='native',
                                    style_table={'overflowX': 'auto'},
                                    style_header={
                                        'backgroundColor': _AZUL,
                                        'color': 'white',
                                        'fontWeight': 'bold',
                                        'textAlign': 'center',
                                    },
                                    style_cell={
                                        'textAlign': 'center',
                                        'padding': '8px 12px',
                                        'fontFamily': 'Roboto, sans-serif',
                                    },
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'Ubicacion'}, 'textAlign': 'left'},
                                    ],
                                    style_data_conditional=[
                                        {'if': {'row_index': 'odd'}, 'backgroundColor': '#eef0f8'},
                                    ],
                                ),
                                className='panel-grafico tabla-sismos',
                                style={**_CARD, 'padding': '10px'},
                            ),
                        ],
                        width=12,
                    ),
                    className='mb-4',
                ),
            ],
            fluid=False,
        ),

        # Footer
        html.Footer(
            [
                'Creado por Ing. ',
                html.A(
                    'Camilo A. Castañeda Galindo',
                    href='https://www.linkedin.com/in/camilocastanedagalindo/',
                    target='_blank',
                    style={'color': 'white', 'textDecoration': 'underline'},
                ),
                ' – 2026',
            ],
            style={
                'backgroundColor': _AZUL,
                'color': 'white',
                'textAlign': 'center',
                'padding': '16px',
                'fontSize': '0.9rem',
            },
        ),
    ],
    style={'backgroundColor': _FONDO, 'minHeight': '100vh', 'paddingBottom': '30px'},
)

