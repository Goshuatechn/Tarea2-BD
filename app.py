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

# Ruta para obtener la lista de puestos
@app.route('/obtener-puestos')
def obtener_puestos():
    try:
        puestos = BD_model.obtenerPuestos()
        print(f"[DEBUG] Puestos obtenidos en la ruta: {puestos}")
        return jsonify(puestos)
    except Exception as e:
        print(f"[ERROR] Error en la ruta /obtener-puestos: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify([])

# Ruta para verificar que no exista un empleado con el mismo documento o nombre
@app.route('/verificar-empleado', methods=['POST'])
def verificar_empleado():
    try:
        empleado = request.json
        print(f"[DEBUG] Datos recibidos para verificar empleado: {empleado}")
        
        # Verificar que los campos requeridos estén presentes
        if not empleado.get('documento_identidad') or not empleado.get('nombre'):
            return jsonify({
                'success': False,
                'message': 'Se requieren tanto el documento de identidad como el nombre'
            }), 400
            
        # Llamar a la función del modelo para verificar el empleado
        try:
            # Llamar a la función de verificación con los nombres de parámetros correctos
            success, message = BD_model.verificarEmpleado(
                documento_identidad=empleado['documento_identidad'],
                nombre=empleado['nombre']
            )
            
            # Si success es False, significa que el empleado ya existe o hay un error
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            
            # Si llegamos aquí, el empleado es válido para registro
            return jsonify({
                'success': True,
                'message': 'Empleado válido para registro'
            })
                
        except Exception as e:
            print(f'[ERROR] Error al verificar empleado: {str(e)}')
            return jsonify({
                'success': False,
                'message': f'Error al verificar el empleado: {str(e)}'
            }), 500
            
    except Exception as e:
        error_msg = f'Error al procesar la solicitud: {str(e)}'
        print(f'[ERROR] {error_msg}')
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': error_msg
        }), 500

# Ruta para agregar un nuevo empleado
@app.route('/agregar-empleado', methods=['POST'])
def agregar_empleado():
    try:
        empleado = request.json
        print(f"[DEBUG] Datos recibidos para nuevo empleado: {empleado}")
        
        # Convertir el estado a booleano
        es_activo = empleado.get('activo', True)
        
        # Llamar a la función del modelo con los parámetros correctos
        success, message = BD_model.agregarEmpleado(
            nombre=empleado['nombre'],
            valor_documento_identidad=empleado['documento_identidad'],
            fecha_contratacion=empleado['fecha_contratacion'],
            id_puesto=empleado['puesto'],
            es_activo=es_activo
        )
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'message': message}), 400
            
    except KeyError as e:
        error_msg = f'Falta el campo requerido: {str(e)}'
        print(f'[ERROR] {error_msg}')
        return jsonify({'success': False, 'message': error_msg}), 400
        
    except Exception as e:
        error_msg = f'Error al procesar la solicitud: {str(e)}'
        print(f'[ERROR] {error_msg}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': error_msg}), 500
    
    return jsonify({'message': 'Empleado agregado correctamente'})

# Ruta para eliminar un empleado
@app.route('/eliminar-empleado/<int:empleado_id>', methods=['DELETE'])
def eliminar_empleado(empleado_id):
    try:
        print(f"[DEBUG] Ruta eliminar_empleado llamada con ID: {empleado_id}")
        print(f"[DEBUG] Tipo de empleado_id: {type(empleado_id)}")
        
        if not empleado_id:
            print("[ERROR] No se proporcionó un ID de empleado")
            return jsonify({'success': False, 'message': 'Se requiere un ID de empleado'}), 400
            
        # Llamar a la función del modelo para eliminar el empleado
        success, message = BD_model.eliminarEmpleado(empleado_id)
        
        if success:
            print(f"[DEBUG] Empleado {empleado_id} eliminado exitosamente")
            return jsonify({'success': True, 'message': message})
        else:
            print(f"[ERROR] Error al eliminar empleado: {message}")
            return jsonify({'success': False, 'message': message}), 400
            
    except Exception as e:
        error_msg = f'Error al procesar la solicitud: {str(e)}'
        print(f'[ERROR] {error_msg}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': error_msg}), 500

# Ruta para modificar un empleado
@app.route('/modificar-empleado/<int:empleado_id>', methods=['PUT'])
def modificar_empleado(empleado_id):
    try:
        print(f"[DEBUG] Ruta modificar_empleado llamada con ID: {empleado_id}")
        
        if not empleado_id:
            return jsonify({'success': False, 'message': 'Se requiere un ID de empleado'}), 400
            
        # Obtener los datos del cuerpo de la petición
        data = request.get_json()
        print(f"[DEBUG] Datos recibidos: {data}")
        
        if not data:
            return jsonify({'success': False, 'message': 'No se proporcionaron datos para actualizar'}), 400
            
        # Llamar a la función del modelo para modificar el empleado
        success, message = BD_model.modificarEmpleado(
            id_empleado=empleado_id,
            valor_documento_identidad=data.get('valor_documento_identidad'),
            nombre=data.get('nombre'),
            id_puesto=data.get('id_puesto')
        )
        
        if success:
            print(f"[DEBUG] Empleado {empleado_id} modificado exitosamente")
            return jsonify({'success': True, 'message': message})
        else:
            print(f"[ERROR] Error al modificar empleado: {message}")
            return jsonify({'success': False, 'message': message}), 400
            
    except Exception as e:
        error_msg = f'Error al procesar la solicitud: {str(e)}'
        print(f'[ERROR] {error_msg}')
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': error_msg}), 500

# Ruta para la página principal
@app.route('/main')
def main():
    return render_template('main.html')

# --------------------------------------------------------------------------------- #
# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=PORT)