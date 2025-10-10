# Librerías
import pyodbc

# Variable global para la conexión
conexion = None

def get_connection():
    global conexion
    if conexion is None:
        try:
            server = r'DESKTOP-A84CP9L\SQLEXPRESS'  # dirección del servidor SQL Server
            database = 'Tarea2BD_dev'
            
            conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={server};'
                f'DATABASE={database};'
                'Trusted_Connection=yes;'
            )
            print("Conexión a SQL Server establecida")
        except pyodbc.Error as err:
            print(f"Error de conexión a SQL Server: {err}")
            raise
    return conexion


def obtenerUsuariosLogin():
    # TODO -> Lógica para retornar todos los usuarios que pueden modificar la base de datos
    pass

# Verificar que no exista un empleado con el mismo documento o nombre
def verificarEmpleado(documento_identidad, nombre):
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if not conn:
            return False, "No se pudo establecer conexión con la base de datos"
            
        cursor = conn.cursor()

        # Verificar si ya existe un empleado con el mismo documento
        cursor.execute("SELECT * FROM dbo.Empleado WHERE ValorDocumentoIdentidad = ?", (documento_identidad,))
        if cursor.fetchone():
            return False, "Ya existe un empleado con este número de documento"

        # Verificar si ya existe un empleado con el mismo nombre
        cursor.execute("SELECT * FROM dbo.Empleado WHERE Nombre = ?", (nombre,))
        if cursor.fetchone():
            return False, "Ya existe un empleado con este nombre"
            
        return True, ""
        
    except Exception as e:
        import traceback
        error_msg = f"Error en verificarEmpleado: {str(e)}\n{traceback.format_exc()}"
        print(f"[ERROR] {error_msg}")
        return False, f"Error al verificar el empleado: {str(e)}"
        
    finally:
        # Solo cerramos el cursor, no la conexión
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                print(f"[ERROR] Error al cerrar el cursor: {str(e)}")
        # No cerramos la conexión aquí, se manejará en el contexto de la solicitud

def obtenerPuestos():
    print("\n[DEBUG] Iniciando obtenerEmpleados()")
    conn = None
    cursor = None
    try:
        # Crear una nueva conexión para esta operación
        print("[DEBUG] Creando nueva conexión...")
        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-A84CP9L\\SQLEXPRESS;'
            'DATABASE=Tarea2BD_dev;'
            'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(connection_string)
        print(f"[DEBUG] Estado de conexión: {'Conectado' if conn else 'Desconectado'}")
        
        # Crear un nuevo cursor
        cursor = conn.cursor()
        print("[DEBUG] Cursor creado exitosamente")
        
        # Consulta para obtener los empleados con información del puesto
        query = "SELECT * FROM dbo.Puesto; "

        cursor.execute(query)
        puestos = []
        
        # Obtener los nombres de las columnas
        columns = [column[0] for column in cursor.description]
        
        # Obtener todas las filas
        rows = cursor.fetchall()
        
        # Convertir los resultados a una lista de diccionarios
        for row in rows:
            try:
                # Crear un diccionario con los nombres de columna correctos
                puesto = dict(zip(columns, row))
                puestos.append(puesto)
            except Exception as e:
                print(f"[ERROR] Error al procesar fila: {row}")
                print(f"[ERROR] Detalles: {str(e)}")
                continue
        
        print(f"[DEBUG] Se encontraron {len(puestos)} puestos")
        return puestos
        
    except Exception as e:
        print(f"[ERROR] Error en obtenerPuestos: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        # Cerrar el cursor si está abierto
        if cursor:
            try:
                cursor.close()
                print("[DEBUG] Cursor cerrado en obtenerPuestos")
            except Exception as e:
                print(f"[ERROR] Error al cerrar el cursor: {str(e)}")
                
        # Cerrar la conexión si está abierta
        if conn:
            try:
                print("[DEBUG] Cerrando conexión en obtenerPuestos")
                conn.close()
                print("[DEBUG] Conexión cerrada exitosamente en obtenerPuestos")
            except Exception as close_error:
                print(f"[ERROR] Error al cerrar la conexión: {str(close_error)}")

def obtenerEmpleados():
    print("\n[DEBUG] Iniciando obtenerEmpleados()")
    conn = None
    cursor = None
    try:
        # Crear una nueva conexión para esta operación
        print("[DEBUG] Creando nueva conexión...")
        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-A84CP9L\\SQLEXPRESS;'
            'DATABASE=Tarea2BD_dev;'
            'Trusted_Connection=yes;'
        )
        conn = pyodbc.connect(connection_string)
        print(f"[DEBUG] Estado de conexión: {'Conectado' if conn else 'Desconectado'}")
        
        # Crear un nuevo cursor
        cursor = conn.cursor()
        print("[DEBUG] Cursor creado exitosamente")
        
        # Consulta para obtener los empleados con información del puesto
        query = """
        SELECT 
            e.Id as id_empleado,
            e.Nombre as nombre,
            e.ValorDocumentoIdentidad as valor_documento_identidad,
            e.FechaContratacion as fecha_contratacion,
            e.SaldoVacaciones as saldo_vacaciones,
            e.EsActivo as es_activo,
            e.IdPuesto as id_puesto,
            p.Nombre as nombre_puesto
        FROM dbo.Empleado e
        LEFT JOIN dbo.Puesto p ON e.IdPuesto = p.Id
        WHERE e.EsActivo = 1  -- Solo empleados activos
        ORDER BY e.Nombre
        """

        cursor.execute(query)
        empleados = []
        
        # Obtener los nombres de las columnas
        columns = [column[0] for column in cursor.description]
        
        # Obtener todas las filas
        rows = cursor.fetchall()
        
        # Convertir los resultados a una lista de diccionarios
        for row in rows:
            try:
                # Crear un diccionario con los nombres de columna correctos
                empleado = dict(zip(columns, row))
                
                # Formatear los datos según sea necesario
                empleado_formateado = {
                    "id_empleado": empleado['id_empleado'],
                    "nombre_completo": empleado['nombre'],
                    "nombre": empleado['nombre'],
                    "documento_identidad": empleado['valor_documento_identidad'],
                    "fecha_contratacion": empleado['fecha_contratacion'].strftime('%Y-%m-%d') if empleado['fecha_contratacion'] else None,
                    "saldo_vacaciones": int(empleado['saldo_vacaciones']) if empleado['saldo_vacaciones'] is not None else 0,
                    "activo": bool(empleado['es_activo']),
                    "puesto": empleado.get('nombre_puesto', 'Sin puesto asignado'),
                    "id_puesto": empleado['id_puesto']
                }
                empleados.append(empleado_formateado)
                
            except Exception as emp_error:
                print(f"[ERROR] Error al procesar empleado: {str(emp_error)}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"[DEBUG] Se encontraron {len(empleados)} empleados")
        return empleados
        
    except Exception as e:
        print(f"[ERROR] Error en obtenerEmpleados: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        # Cerrar el cursor si está abierto
        if cursor:
            try:
                cursor.close()
                print("[DEBUG] Cursor cerrado")
            except Exception as e:
                print(f"[ERROR] Error al cerrar el cursor: {str(e)}")
                
        # Cerrar la conexión si está abierta
        if conn:
            try:
                print("[DEBUG] Cerrando conexión en obtenerEmpleados")
                conn.close()
                print("[DEBUG] Conexión cerrada exitosamente")
            except Exception as close_error:
                print(f"[ERROR] Error al cerrar la conexión: {str(close_error)}")
                
        print("[DEBUG] Finalizado obtenerEmpleados")

def agregarEmpleado(nombre, valor_documento_identidad, fecha_contratacion, id_puesto, saldo_vacaciones=0, es_activo=True, id_post_by_user=None, post_in_ip=None):
    print("\n[DEBUG] Iniciando agregarEmpleado()")
    
    # Obtener la conexión existente
    conn = get_connection()
    cursor = None
    
    try:
        print(f"[DEBUG] Usando conexión existente: {'Conectado' if conn else 'Desconectado'}")
        
        # Verificar si la conexión está activa
        if conn is None:
            print("[ERROR] No hay conexión disponible")
            return False, "Error: No hay conexión a la base de datos"
            
        # Crear un nuevo cursor
        cursor = conn.cursor()
        print("[DEBUG] Cursor creado exitosamente")
        
        # Llamar al stored procedure
        print("[DEBUG] Ejecutando SP_InsertarEmpleado con los siguientes parámetros:")
        print(f"[DEBUG] - Nombre: {nombre}")
        print(f"[DEBUG] - Documento: {valor_documento_identidad}")
        print(f"[DEBUG] - Puesto ID: {id_puesto}")
        print(f"[DEBUG] - Fecha Contratación: {fecha_contratacion}")
        
        # Llamar al stored procedure con parámetros de salida
        sql = """
        DECLARE @outNuevoID INT;
        DECLARE @outResultCode INT;
        
        EXEC SP_InsertarEmpleado 
            @inValorDocumentoIdentidad = ?,
            @inNombre = ?,
            @inIdPuesto = ?,
            @inFechaContratacion = ?,
            @inIdPostByUser = ?,
            @inPostInIP = ?,
            @outNuevoID = @outNuevoID OUTPUT,
            @outResultCode = @outResultCode OUTPUT;
            
        SELECT @outNuevoID, @outResultCode;
        """
        
        # Ejecutar la consulta
        cursor.execute(sql, (
            str(valor_documento_identidad),
            str(nombre),
            int(id_puesto),
            str(fecha_contratacion),
            int(id_post_by_user) if id_post_by_user else None,
            str(post_in_ip) if post_in_ip else None
        ))
        
        # Obtener los resultados
        result = cursor.fetchone()
        if result:
            nuevo_id = result[0]
            result_code = result[1]
            
            # Mapear códigos de resultado a mensajes
            error_messages = {
                0: "Empleado agregado correctamente",
                50004: "Ya existe un empleado con este número de documento",
                50005: "Ya existe un empleado con este nombre",
                50008: "Error en la base de datos al insertar el empleado",
                50009: "El nombre contiene caracteres inválidos",
                50010: "El número de documento contiene caracteres inválidos (solo números permitidos)",
                50011: "La fecha de contratación no puede ser futura",
                50012: "El ID del puesto no existe"
            }
            
            if result_code == 0:
                conn.commit()
                print(f"[DEBUG] Empleado agregado correctamente con ID: {nuevo_id}")
                return True, error_messages[result_code]
            else:
                error_msg = error_messages.get(result_code, f"Error desconocido (Código: {result_code})")
                print(f"[ERROR] Error al agregar empleado: {error_msg}")
                conn.rollback()
                return False, error_msg
        else:
            print("[ERROR] No se recibió respuesta del procedimiento almacenado")
            conn.rollback()
            return False, "No se pudo obtener el resultado de la operación"
            
    except pyodbc.Error as e:
        error_msg = str(e).replace('\n', ' ').replace('\r', '')
        print(f"[ERROR] Error de base de datos en agregarEmpleado: {error_msg}")
        if conn:
            conn.rollback()
        return False, f"Error de base de datos: {error_msg}"
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        print("[ERROR] Excepción inesperada en agregarEmpleado:")
        traceback.print_exc()
        if conn:
            conn.rollback()
        return False, f"Error inesperado al agregar empleado: {error_msg}"
        
    finally:
        # Cerrar solo el cursor, no la conexión
        if cursor:
            try:
                cursor.close()
                print("[DEBUG] Cursor cerrado correctamente")
            except Exception as e:
                print(f"[ERROR] Error al cerrar el cursor: {str(e)}")
        
        # No cerramos la conexión aquí, se manejará en el contexto de la solicitud

def modificarEmpleado(id_empleado, valor_documento_identidad, nombre, id_puesto, id_post_by_user=1, post_in_ip='127.0.0.1'):
    conn = None
    cursor = None
    
    print("\n[DEBUG] Iniciando modificarEmpleado()")
    print(f"[DEBUG] ID del empleado: {id_empleado}")
    print(f"[DEBUG] Documento de identidad: {valor_documento_identidad}")
    print(f"[DEBUG] Nombre: {nombre}")
    print(f"[DEBUG] ID del puesto: {id_puesto}")
    print(f"[DEBUG] ID del usuario que realiza la modificación: {id_post_by_user}")
    print(f"[DEBUG] IP del usuario que realiza la modificación: {post_in_ip}")
    
    try:
        conn = get_connection()
        if not conn:
            return False, "No se pudo establecer conexión con la base de datos"
            
        cursor = conn.cursor()
        
        # Llamar al stored procedure SP_ActualizarEmpleado
        params = (
            id_empleado,
            valor_documento_identidad,
            nombre,
            id_puesto,
            id_post_by_user,
            post_in_ip
        )
        
        # Ejecutar el stored procedure
        cursor.execute("""
            DECLARE @outResultCode INT;
            EXEC SP_ActualizarEmpleado 
                @inId = ?,
                @inValorDocumentoIdentidad = ?,
                @inNombre = ?,
                @inIdPuesto = ?,
                @inIdPostByUser = ?,
                @inPostInIP = ?,
                @outResultCode = @outResultCode OUTPUT;
            SELECT @outResultCode as result_code;
        """, params)
        
        # Obtener el código de resultado
        result_code = cursor.fetchone().result_code
        
        if result_code == 0:
            conn.commit()
            return True, "Empleado actualizado exitosamente"
        else:
            conn.rollback()
            return False, f"Error al actualizar empleado (Código: {result_code})"
            
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error al actualizar empleado: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, str(e)
    finally:
        if cursor:
            cursor.close()
        # No cerramos la conexión aquí, se manejará en el contexto de la solicitud

def eliminarEmpleado(id_empleado, id_post_by_user=1, post_in_ip='127.0.0.1'):
    
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado
        sql = """
        DECLARE @outResultCode INT;
        
        EXEC SP_EliminarEmpleado 
            @inId = ?,
            @inIdPostByUser = ?,
            @inPostInIP = ?,
            @outResultCode = @outResultCode OUTPUT;
            
        SELECT @outResultCode as result_code;
        """
        
        # Ejecutar la consulta con parámetros
        cursor.execute(sql, (id_empleado, id_post_by_user, post_in_ip))
        result = cursor.fetchone()
        result_code = result.result_code if result else -1
        
        # Mapear códigos de resultado a mensajes
        result_messages = {
            0: "Empleado eliminado correctamente",
            50001: "El ID del empleado no puede ser nulo",
            50002: "No se encontró el empleado con el ID proporcionado",
            50003: "Error en la base de datos al eliminar el empleado"
        }
        
        if result_code == 0:
            conn.commit()
            return True, result_messages[result_code]
        else:
            error_msg = result_messages.get(result_code, f"Error desconocido (Código: {result_code})")
            return False, error_msg
            
    except Exception as e:
        import traceback
        error_msg = f"Error al eliminar empleado: {str(e)}\n{traceback.format_exc()}"
        print(f"[ERROR] {error_msg}")
        if conn:
            conn.rollback()
        return False, f"Error al eliminar empleado: {str(e)}"
        
    finally:
        # Cerrar cursor y conexión
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                print(f"[ERROR] Error al cerrar el cursor: {str(e)}")
        # No cerramos la conexión aquí, se manejará en el contexto de la solicitud


    
