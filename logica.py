# Lógica: callbacks de la aplicación
from datetime import datetime

import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Output, Input, html
import dash_bootstrap_components as dbc
from folium.plugins import HeatMap
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans

from app import app
from data import consultar_sismos, filtrar_tolima, rango_fechas_ultima_semana

_CENTRO_TOLIMA = {'lat': 4.5, 'lon': -75.2}

_KPI_COLOR = {
    'total': '#00184a',
    'mag_max': '#c0392b',
    'mag_prom': '#e07b7b',
    'prof_prom': '#2f6fa8',
}


def build_mapa_satelital(dff):
    mapa = folium.Map(
        location=[_CENTRO_TOLIMA['lat'], _CENTRO_TOLIMA['lon']],
        zoom_start=8,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
    )
    for _, row in dff.iterrows():
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=f'Magnitud: {row["mag"]} - Profundidad: {row["depth"]} km - {row["place"]}',
        ).add_to(mapa)
    return mapa.get_root().render()


def build_mapa_calor(dff):
    mapa = folium.Map(location=[_CENTRO_TOLIMA['lat'], _CENTRO_TOLIMA['lon']], zoom_start=8)
    datos_calor = dff[['latitud', 'longitud']].dropna().values.tolist()
    if datos_calor:
        HeatMap(datos_calor, radius=15).add_to(mapa)
    return mapa.get_root().render()


def build_mapa_plotly(dff):
    fig = px.scatter_mapbox(
        dff,
        lat='latitud',
        lon='longitud',
        color='mag',
        size='mag',
        hover_name='place',
        hover_data={'depth': True, 'utcTime': True, 'latitud': False, 'longitud': False},
        zoom=7,
        center=_CENTRO_TOLIMA,
    )
    fig.update_layout(
        mapbox_style='open-street-map',
        margin=dict(r=0, t=10, l=0, b=0),
    )
    return fig


def build_serie_diaria(dff):
    serie = dff.set_index('utcTime').sort_index().resample('D').size()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=serie.index, y=serie.values, mode='lines+markers'))
    fig.update_layout(
        template='plotly_white',
        xaxis_title='<b>Fecha</b>',
        yaxis_title='<b>Cantidad de sismos</b>',
        margin=dict(l=50, r=20, t=20, b=50),
    )
    return fig


def build_distribucion(dff):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Distribución de magnitudes', 'Distribución de profundidades'))
    fig.add_trace(go.Histogram(x=dff['mag'], nbinsx=15, marker_color='#00184a'), row=1, col=1)
    fig.add_trace(go.Histogram(x=dff['depth'], nbinsx=15, marker_color='#e07b7b'), row=1, col=2)
    fig.update_xaxes(title_text='Magnitud', row=1, col=1)
    fig.update_xaxes(title_text='Profundidad (km)', row=1, col=2)
    fig.update_layout(template='plotly_white', showlegend=False, margin=dict(l=40, r=20, t=40, b=40))
    return fig


def build_mag_profundidad(dff):
    fig = px.scatter(
        dff, x='depth', y='mag', opacity=0.7,
        labels={'depth': 'Profundidad (km)', 'mag': 'Magnitud'},
    )
    fig.update_layout(template='plotly_white', margin=dict(l=50, r=20, t=20, b=50))
    return fig


def build_top_ubicaciones(dff):
    top_lugares = dff['place'].value_counts().head(15).sort_values()
    fig = px.bar(
        x=top_lugares.values, y=top_lugares.index, orientation='h',
        labels={'x': 'Cantidad de sismos', 'y': ''},
    )
    fig.update_layout(template='plotly_white', margin=dict(l=10, r=20, t=20, b=40))
    return fig


def build_patron_horario(dff):
    horas = dff['localTime'].dt.hour.value_counts().sort_index()
    fig = px.bar(x=horas.index, y=horas.values, labels={'x': 'Hora', 'y': 'Cantidad de sismos'})
    fig.update_layout(template='plotly_white', margin=dict(l=50, r=20, t=20, b=50))
    return fig


def build_clusters(dff):
    coords = dff[['latitud', 'longitud']].dropna()
    n_clusters = min(5, len(coords))
    if n_clusters < 1:
        return px.scatter_mapbox()
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_clusters = coords.copy()
    df_clusters['cluster'] = kmeans.fit_predict(coords).astype(str)
    fig = px.scatter_mapbox(
        df_clusters, lat='latitud', lon='longitud', color='cluster',
        zoom=7, center=_CENTRO_TOLIMA,
    )
    fig.update_layout(mapbox_style='open-street-map', margin=dict(r=0, t=10, l=0, b=0))
    return fig


def _tarjeta_kpi(icono, valor, etiqueta, color):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.I(className=f'bi {icono}', style={'fontSize': '1.6rem', 'opacity': '0.85'}),
                    html.Div(valor, className='kpi-valor'),
                    html.Div(etiqueta, className='kpi-etiqueta'),
                ],
                style={'textAlign': 'center'},
            ),
            className='tarjeta-kpi',
            style={'backgroundColor': color},
        ),
        xs=6, lg=3,
    )


def build_kpis(dff):
    total = len(dff)
    mag_max = dff['mag'].max()
    mag_prom = dff['mag'].mean()
    prof_prom = dff['depth'].mean()
    return [
        _tarjeta_kpi('bi-activity', f'{total}', 'Sismos registrados', _KPI_COLOR['total']),
        _tarjeta_kpi('bi-exclamation-triangle', f'{mag_max:.1f}', 'Magnitud máxima', _KPI_COLOR['mag_max']),
        _tarjeta_kpi('bi-speedometer2', f'{mag_prom:.1f}', 'Magnitud promedio', _KPI_COLOR['mag_prom']),
        _tarjeta_kpi('bi-arrow-down-circle', f'{prof_prom:.0f} km', 'Profundidad promedio', _KPI_COLOR['prof_prom']),
    ]


def build_tabla(dff):
    tabla = dff.sort_values('utcTime', ascending=False).copy()
    return [
        {
            'Fecha': fila['localTime'].strftime('%Y-%m-%d'),
            'Hora': fila['localTime'].strftime('%H:%M:%S'),
            'Ubicacion': fila['place'],
            'Magnitud': fila['mag'],
            'Profundidad': fila['depth'],
        }
        for _, fila in tabla.iterrows()
    ]


def _figura_vacia(mensaje):
    fig = go.Figure()
    fig.update_layout(
        template='plotly_white',
        annotations=[dict(text=mensaje, x=0.5, y=0.5, showarrow=False, font=dict(size=14))],
        xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return fig


@app.callback(
    Output('banner-actualizacion', 'children'),
    Output('mensaje-sin-datos', 'children'),
    Output('fila-kpis', 'children'),
    Output('iframe-satelital', 'srcDoc'),
    Output('graph-mapa-plotly', 'figure'),
    Output('graph-serie-diaria', 'figure'),
    Output('graph-distribucion', 'figure'),
    Output('graph-mag-profundidad', 'figure'),
    Output('graph-top-ubicaciones', 'figure'),
    Output('graph-patron-horario', 'figure'),
    Output('iframe-calor', 'srcDoc'),
    Output('graph-clusters', 'figure'),
    Output('tabla-sismos', 'data'),
    Input('interval-actualizacion', 'n_intervals'),
)
# Se ejecuta al cargar la página y luego cada 30 minutos (dcc.Interval), consultando de nuevo la API y regenerando todas las visualizaciones
def actualizar_dashboard(n_intervals):
    startdate, enddate = rango_fechas_ultima_semana()
    df = consultar_sismos()
    dff = filtrar_tolima(df)

    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    banner = (
        f'Rango consultado: {startdate[:10]} a {enddate[:10]}  |  '
        f'Última actualización: {ahora}  |  Sismos en el Tolima: {len(dff)}'
    )

    if dff.empty:
        mensaje = html.Div(
            'No se registraron sismos con epicentro en el Tolima durante el rango consultado.',
            style={'textAlign': 'center', 'color': '#a00', 'fontWeight': '600', 'padding': '10px'},
        )
        fig_vacia = _figura_vacia('Sin datos para mostrar')
        mapa_vacio = folium.Map(location=[_CENTRO_TOLIMA['lat'], _CENTRO_TOLIMA['lon']], zoom_start=8).get_root().render()
        kpis_vacios = [
            _tarjeta_kpi('bi-activity', '0', 'Sismos registrados', _KPI_COLOR['total']),
            _tarjeta_kpi('bi-exclamation-triangle', 'N/A', 'Magnitud máxima', _KPI_COLOR['mag_max']),
            _tarjeta_kpi('bi-speedometer2', 'N/A', 'Magnitud promedio', _KPI_COLOR['mag_prom']),
            _tarjeta_kpi('bi-arrow-down-circle', 'N/A', 'Profundidad promedio', _KPI_COLOR['prof_prom']),
        ]
        return (
            banner, mensaje, kpis_vacios, mapa_vacio, fig_vacia, fig_vacia,
            fig_vacia, fig_vacia, fig_vacia, fig_vacia, mapa_vacio, fig_vacia, [],
        )

    return (
        banner,
        None,
        build_kpis(dff),
        build_mapa_satelital(dff),
        build_mapa_plotly(dff),
        build_serie_diaria(dff),
        build_distribucion(dff),
        build_mag_profundidad(dff),
        build_top_ubicaciones(dff),
        build_patron_horario(dff),
        build_mapa_calor(dff),
        build_clusters(dff),
        build_tabla(dff),
    )

