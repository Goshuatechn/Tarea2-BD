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
            username = ''  # usuario de SQL Server
            password = ''  # contraseña
            
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

def obtenerEmpleados():
    
    try:
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Consulta para obtener los empleados con información del puesto
        query = """
        SELECT 
            e.Id as id_empleado,
            e.Nombre as nombre,
            e.ValorDocumentoIdentidad as documento_identidad,
            e.FechaContratacion as fecha_contratacion,
            e.SaldoVacaciones as saldo_vacaciones,
            e.EsActivo as activo,
            e.IdPuesto as id_puesto,
            p.Nombre as nombre_puesto
        FROM dbo.Empleado e
        LEFT JOIN dbo.Puesto p ON e.IdPuesto = p.Id
        WHERE e.EsActivo = 1  -- Solo empleados activos
        ORDER BY e.Nombre
        """

        cursor.execute(query)
        empleados = []
        
        rows = cursor.fetchall()
        
        # Convertir los resultados a una lista de diccionarios
        for i, row in enumerate(rows, 1):
            try:
                empleado = {
                    "id_empleado": row.id_empleado,
                    "nombre_completo": row.nombre,
                    "nombre": row.nombre,
                    "documento_identidad": row.documento_identidad,
                    "fecha_contratacion": row.fecha_contratacion.strftime('%Y-%m-%d') if row.fecha_contratacion else None,
                    "saldo_vacaciones": int(row.saldo_vacaciones) if row.saldo_vacaciones is not None else 0,
                    "activo": bool(row.activo),
                    "puesto": row.nombre_puesto if hasattr(row, 'nombre_puesto') and row.nombre_puesto else "Sin puesto asignado",
                    "id_puesto": row.id_puesto
                }
                empleados.append(empleado)
                
            except Exception as emp_error:
                import traceback
                traceback.print_exc()
                continue
        
        # print("[DEBUG] Empleados obtenidos correctamente: ", empleados)
        

        return empleados
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return []
    finally:
        if 'conn' in locals() and conn:
            try:
                conn.close()
                print("[DEBUG] Conexión a la base de datos cerrada")
            except Exception as close_error:
                print("[ERROR] Error al cerrar la conexión")
                import traceback
                traceback.print_exc()

def agregarEmpleado(nombre, valor_documento_identidad, fecha_contratacion, id_puesto, saldo_vacaciones=0, es_activo=True):
    """
    Agrega un nuevo empleado a la base de datos.
    
    Args:
        nombre (str): Nombre completo del empleado
        valor_documento_identidad (str): Número de documento de identidad
        fecha_contratacion (str): Fecha de contratación en formato 'YYYY-MM-DD'
        id_puesto (int): ID del puesto del empleado
        saldo_vacaciones (int, optional): Días de vacaciones disponibles. Defaults to 0.
        es_activo (bool, optional): Estado del empleado. Defaults to True (activo).
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe un empleado con el mismo documento de identidad
        cursor.execute("SELECT Id FROM dbo.Empleado WHERE ValorDocumentoIdentidad = ?", 
                      (valor_documento_identidad,))
        if cursor.fetchone() is not None:
            return False, "Ya existe un empleado con este número de documento"
        
        query = """
        INSERT INTO dbo.Empleado 
            (Nombre, ValorDocumentoIdentidad, FechaContratacion, IdPuesto, SaldoVacaciones, EsActivo)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            nombre,
            valor_documento_identidad,
            fecha_contratacion,
            id_puesto,
            saldo_vacaciones,
            1 if es_activo else 0
        ))
        
        conn.commit()
        return True, "Empleado agregado correctamente"
        
    except pyodbc.Error as e:
        error_msg = str(e).replace('\n', ' ').replace('\r', '')
        print(f"[ERROR] Error al agregar empleado: {error_msg}")
        return False, f"Error al agregar empleado: {error_msg}"
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Error inesperado al agregar empleado: {str(e)}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def actualizarEmpleado(id_empleado, nombre, apellido, fecha_ingreso=None, salario=None, id_departamento=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        UPDATE dbo.Empleado
        SET nombre = ?, apellido = ?, fecha_ingreso = ?, 
            salario = ?, id_departamento = ?
        WHERE id_empleado = ?
        """
        
        cursor.execute(query, (nombre, apellido, fecha_ingreso, salario, id_departamento, id_empleado))
        conn.commit()
        return True, "Empleado actualizado correctamente"
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Error al actualizar empleado: {str(e)}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def eliminarEmpleado(id_empleado):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM dbo.Empleado WHERE id_empleado = ?"
        cursor.execute(query, (id_empleado,))
        conn.commit()
        
        if cursor.rowcount > 0:
            return True, "Empleado eliminado correctamente"
        else:
            return False, "No se encontró el empleado con el ID proporcionado"
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Error al eliminar empleado: {str(e)}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()


    
