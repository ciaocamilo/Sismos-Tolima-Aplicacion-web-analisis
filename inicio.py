# Punto de inicio de la aplicación
import os
from app import app
from gui import layout
import logica

# app es el objeto principal de Dash (creado en app.py), y su propiedad .layout define qué se renderiza en el navegador
# Al asignarle layout (importado desde gui.py), le estamos diciendo a Dash: "este es el árbol de componentes que debe mostrar como página web"
app.layout = layout

if __name__ == '__main__':
    # Para ejecutar la aplicación, se obtiene el puerto desde la variable de entorno PORT (útil para despliegues en plataformas como Render) o se usa el puerto 8050 por defecto
    port = int(os.environ.get('PORT', 8050))
    # Finalmente, se ejecuta la aplicación con app.run(), indicando que no se active el modo debug (debug=False) y que escuche en todas las interfaces de red (host='0.0.0.0')
    app.run(debug=False, host='0.0.0.0', port=port)