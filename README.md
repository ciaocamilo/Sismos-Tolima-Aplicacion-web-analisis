# Aplicación web interactiva para el análisis de sismos en el Tolima

---

#### Creada por:
Ing. Camilo Andrés Castañeda Galindo

---

## Índice

1. [Introducción del proyecto](#1-introducción-del-proyecto)
2. [Objetivo](#2-objetivo)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Requisitos](#4-requisitos)
5. [Despliegue en Render](#5-despliegue-en-render)
6. [Software](#6-software)
7. [Instalación](#7-instalación)
8. [Visualizaciones](#8-visualizaciones)

---

## 1. Introducción del proyecto

Esta aplicación web interactiva consulta en tiempo real el endpoint público de sismicidad del **Servicio Geológico Colombiano (SGC)** y analiza los eventos sísmicos con epicentro en el **departamento del Tolima**. La aplicación está construida con **Dash** (framework de Python sobre Flask) y hace uso de **Plotly** y **Folium** para la generación de mapas y gráficos dinámicos.

El rango de fechas consultado es **fijo**: desde hace una semana hasta el momento actual. La información se recarga automáticamente **cada 30 minutos** mediante un componente `dcc.Interval`, sin necesidad de recargar la página.

---

## 2. Objetivo

Analizar los patrones de sismicidad en el Tolima a través de visualizaciones interactivas que permitan identificar:

- La ubicación geográfica de los epicentros (vista satelital, mapa interactivo y mapa de calor).
- La evolución diaria de la cantidad de sismos.
- La distribución de magnitudes y profundidades.
- La relación entre magnitud y profundidad.
- Los municipios/zonas con mayor cantidad de sismos.
- El patrón horario de ocurrencia.
- Agrupaciones espaciales (clusters) de los epicentros mediante KMeans.

---

## 3. Estructura del proyecto

```
Sismos-Tolima-Aplicacion-web-analisis/
│
├── inicio.py          # Punto de entrada: asigna el layout y lanza el servidor
├── app.py             # Instancia de la aplicación Dash y configuración base
├── gui.py             # Capa gráfica: definición del layout de la aplicación
├── logica.py          # Callback de actualización (dcc.Interval) y generadores de figuras
├── data.py            # Consulta al endpoint del SGC y transformación de los datos
│
├── requirements.txt   # Dependencias del proyecto con versiones fijadas
├── README.md          # Documentación del proyecto
│
└── assets/
    ├── custom.css     # Estilos personalizados de la aplicación
    └── favicon.svg    # Ícono de la pestaña del navegador
```

---

## 4. Requisitos

Python **3.10+** y las siguientes librerías (versiones exactas en `requirements.txt`):

| Librería | Versión |
|---|---|
| dash | 4.1.0 |
| dash-bootstrap-components | 2.0.4 |
| plotly | 6.7.0 |
| pandas | 3.0.3 |
| numpy | 2.4.5 |
| folium | 0.20.0 |
| scikit-learn | 1.9.1 |
| Flask | 3.1.3 |
| requests | 2.34.2 |

> Las demás dependencias transitivas (Werkzeug, Jinja2, scipy, joblib, etc.) se instalan automáticamente con `pip install -r requirements.txt`.

---

## 6. Software

| Herramienta | Versión / Descripción |
|---|---|
| Python | 3.10 o superior |
| Dash | Framework web para aplicaciones de datos en Python |
| Plotly | Motor de visualizaciones interactivas |
| Folium | Mapas interactivos basados en Leaflet |
| scikit-learn | Clustering espacial (KMeans) |
| Pandas | Manipulación y análisis de datos tabulares |
| Dash Bootstrap Components | Componentes de interfaz basados en Bootstrap 5 |
| VS Code | Editor de código utilizado durante el desarrollo |
| Render | Plataforma de despliegue en la nube (PaaS) |

---

## 7. Instalación

### Crear y activar un entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación

```bash
python inicio.py
```

Abrir el navegador en `http://localhost:8050`.

---

## 8. Visualizaciones

La aplicación consulta el endpoint `https://api.sgc.gov.co/biweekly/biweekly_earthquakes` filtrando los sismos con epicentro (`place`) en el Tolima, y presenta:

1. **Vista satelital** (Folium) con marcadores por sismo (magnitud, profundidad y lugar).
2. **Mapa interactivo** (Plotly) coloreado y dimensionado por magnitud.
3. **Serie diaria** de cantidad de sismos.
4. **Distribución de magnitudes y profundidades** (histogramas).
5. **Magnitud vs. Profundidad** (dispersión).
6. **Top 15 ubicaciones** con más sismos registrados.
7. **Patrón horario** de ocurrencia (hora local).
8. **Mapa de calor** de densidad de epicentros (Folium).
9. **Clusters espaciales** de epicentros mediante KMeans.

Un banner superior indica el rango de fechas consultado, la hora de la última actualización y el total de sismos encontrados en el Tolima. Si no hay sismos registrados en el rango, se muestra un mensaje informativo en lugar de gráficos vacíos.
