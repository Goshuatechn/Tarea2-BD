# Model
import BD_model

# Librerías
from flask import Flask, render_template, request, jsonify, session
from functools import wraps

# Crear la app
app = Flask(__name__)
app.secret_key = '1233'  # Necesaria para usar sesiones
PORT = 5500

# Configuraciones
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Recargar plantillas en hosting time

# --------------------------------------------------------------------------------- #
# Rutas

# Ruta principal
@app.route('/')
def index():
    return render_template('login.html')

# Ruta para obtener empleados
@app.route('/obtener-empleados')
def obtener_empleados():
    empleados = BD_model.obtenerEmpleados()
    return {'empleados': empleados}

@app.route('/main')
def main():
    return render_template('main.html')

# --------------------------------------------------------------------------------- #
# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)