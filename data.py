# Consulta y transformación de datos de sismos (API del Servicio Geológico Colombiano)
from datetime import datetime, timedelta

import pandas as pd
import requests

URL_BASE = 'https://api.sgc.gov.co/biweekly/biweekly_earthquakes'

# Columnas esperadas en el DataFrame final, para poder devolver un DataFrame
# vacío con la misma estructura cuando la API no responde o no hay resultados
COLUMNAS_SISMOS = [
    'id_sismo', 'status', 'rms', 'updated', 'felt', 'sm', 'earthquakeType',
    'magType', 'agency', 'cdi', 'closerTowns', 'gap', 'utcTime', 'localTime',
    'place', 'mag', 'mmi', 'nst', 'depth', 'longitud', 'latitud', 'profundidad_geom',
]


def rango_fechas_ultima_semana():
    # Rango fijo: desde hace 7 días hasta el momento actual
    hoy = datetime.now()
    hace_una_semana = hoy - timedelta(days=7)
    return hace_una_semana.isoformat(), hoy.isoformat()


def consultar_sismos():
    # Descarga y transforma los sismos reportados durante la última semana
    startdate, enddate = rango_fechas_ultima_semana()
    url = f'{URL_BASE}?startdate={startdate}&enddate={enddate}'
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    return _procesar_datos(data)


def _procesar_datos(data):
    features = data.get('features', [])
    if not features:
        return pd.DataFrame(columns=COLUMNAS_SISMOS)

    # json_normalize aplana el diccionario "properties" de cada feature en columnas
    df = pd.json_normalize(features, sep='_')

    # Se extraen longitud, latitud y profundidad desde geometry.coordinates
    coords = df['geometry_coordinates'].apply(pd.Series)
    df['longitud'] = coords[0]
    df['latitud'] = coords[1]
    df['profundidad_geom'] = coords[2]

    # Se descartan columnas redundantes/anidadas que ya no se necesitan
    df = df.drop(columns=['geometry_type', 'geometry_coordinates', 'type'], errors='ignore')

    # Se renombra la columna id de la feature para evitar ambigüedad con properties_*
    df = df.rename(columns={'id': 'id_sismo'})

    # Se quita el prefijo "properties_" de las columnas provenientes de properties
    df.columns = [col.removeprefix('properties_') for col in df.columns]

    # Se convierten las columnas de fecha/hora a tipo datetime
    for col in ['utcTime', 'localTime', 'updated']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    return df


def filtrar_tolima(df):
    # Sismos con epicentro (place) en el departamento del Tolima
    if df.empty or 'place' not in df.columns:
        return df
    return df[df['place'].str.contains('Tolima', case=False, na=False)]
