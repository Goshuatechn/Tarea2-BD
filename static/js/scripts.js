
// Estado de autenticación
const AUTH_PARAM = 'from_login';

// ------------------------------------------------------------ //
// Funciones
// ------------------------------------------------------------ //

// Validar usuario (TODO -> Implementar con base de datos)
function validarUsuario(username, password) {
    
    const usuarios = [
        { username: 'admin', password: 'admin' },
        { username: 'user', password: 'user' }
    ];

    // const usuarios = BD_model.obtenerUsuariosLogin();

    for (let i = 0; i < usuarios.length; i++) {
        if (usuarios[i].username === username && usuarios[i].password === password) {
            return true;
        }
    }

    return false;
}

// Obtener empleados desde BD_model
async function obtenerEmpleados() {
    try {
        const response = await fetch('/obtener-empleados');
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const data = await response.json();
        return data.empleados || [];
    } catch (error) {
        console.error('Error al obtener empleados:', error);
        return [];
    }
}

// Obtener puestos desde el servidor
async function obtenerPuestos() {
    try {
        console.log('[DEBUG] Obteniendo puestos del servidor...');
        const response = await fetch('/obtener-puestos');
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const puestos = await response.json();
        console.log('[DEBUG] Puestos recibidos:', puestos);
        return Array.isArray(puestos) ? puestos : [];
    } catch (error) {
        console.error('Error al obtener puestos:', error);
        return [];
    }
}

// Cargar puestos en el select
async function cargarPuestos(selectId = 'puesto') {
    const selectPuesto = document.getElementById(selectId);
    if (!selectPuesto) {
        console.error(`[ERROR] No se encontró el elemento select con id "${selectId}"`);
        return;
    }
    
    try {
        console.log('[DEBUG] Cargando puestos...');
        const puestos = await obtenerPuestos();
        
        // Limpiar opciones existentes excepto la primera (placeholder)
        while (selectPuesto.options.length > 1) {
            selectPuesto.remove(1);
        }
        
        console.log(`[DEBUG] Se encontraron ${puestos.length} puestos`);
        console.log('[DEBUG] Puestos recibidos:', puestos);
        
        if (puestos.length === 0) {
            console.warn('[ADVERTENCIA] No se encontraron puestos en la base de datos');
            return;
        }
        
        // Agregar opciones de puestos
        puestos.forEach(puesto => {
            try {
                const option = document.createElement('option');
                // Usar 'Id' y 'Nombre' que son las propiedades que vienen del servidor
                option.value = puesto.Id;  // Notar la 'I' mayúscula
                option.textContent = puesto.Nombre;  // Notar la 'N' mayúscula
                selectPuesto.appendChild(option);
            } catch (error) {
                console.error('Error al crear opción de puesto:', error, 'Puesto:', puesto);
            }
        });
        
        console.log('[DEBUG] Puestos cargados correctamente en el select');
    } catch (error) {
        console.error('Error al cargar puestos:', error);
    }
}

// Cargar empleados en la tabla
async function cargarEmpleados() {
    const contenedorFilas = document.getElementById('contenedor_filas_empleados');
    
    // Mostrar indicador de carga
    contenedorFilas.innerHTML = '<div class="cargando">Cargando empleados...</div>';
    
    try {
        const empleados = await obtenerEmpleados();
        
        if (empleados.length === 0) {
            contenedorFilas.innerHTML = '<div class="sin-datos">No se encontraron empleados</div>';
            return;
        }
        
        contenedorFilas.innerHTML = '';
        
        empleados.forEach(empleado => {
            const fila = document.createElement('div');
            fila.className = 'empleado_fila';
            fila.dataset.id = empleado.id_empleado;
            
            // Formatear fecha
            const fechaContratacion = empleado.fecha_contratacion 
                ? new Date(empleado.fecha_contratacion).toLocaleDateString() 
                : 'No especificada';
                
            // Estado como texto
            const estado = empleado.activo ? 'Activo' : 'Inactivo';
            
            fila.innerHTML = `
                <div class="empleado_id">${empleado.id_empleado || 'N/A'}</div>
                <div class="empleado_nombre">${empleado.nombre || 'Sin nombre'}</div>
                <div class="empleado_documento">${empleado.documento_identidad || 'N/A'}</div>
                <div class="empleado_fecha_contratacion">${fechaContratacion}</div>
                <div class="empleado_puesto">${empleado.puesto || 'Sin puesto'}</div>
                <div class="empleado_vacaciones">${empleado.saldo_vacaciones || 0} días</div>
            `;
            contenedorFilas.appendChild(fila);
        });
    
    } catch (error) {
        console.error('Error al cargar empleados:', error);
        contenedorFilas.innerHTML = `
            <div class="error">
                Error al cargar los empleados. ${error.message || 'Intente nuevamente.'}
            </div>`;
    }
}

// ------------------------------------------------------------ //
// Eventos
// ------------------------------------------------------------ //

const ingresarButton = document.getElementById('ingresar_button');
if (ingresarButton) {
    ingresarButton.addEventListener('click', function(a) {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        a.preventDefault();
        
        if (validarUsuario(username, password)) {
            // Marcar como autenticado antes de redirigir
            console.log("Redirigiendo a main...");
            // Agregar parámetro a la URL para indicar que viene de un login exitoso
            window.location.href = '/main?' + new URLSearchParams({ [AUTH_PARAM]: 'true' });
        } else {
            alert('Usuario o contraseña incorrectos');
        }
    });
}

// Función para mostrar el modal de movimientos (TODO -> Verificar la estructura de los movimientos y carga desde la base de datos)
function mostrarModalMovimientos() {
    const modal = document.getElementById('modal_movimientos');
    modal.classList.add('mostrar');
    document.body.style.overflow = 'hidden'; // Evitar scroll del fondo

    // Cargar los movimientos del empleado seleccionado
    // Por ahora solo se muestra un mensaje de ejemplo
    const contenedorMovimientos = document.querySelector('#contenedor_movimientos');
    contenedorMovimientos.innerHTML = `
        <div class="movimiento">
            <div class="movimiento-fecha">2023-10-19</div>
            <div class="movimiento-descripcion">Día de vacaciones</div>
            <div class="movimiento-dias">-1 día</div>
        </div>
        <div class="movimiento">
            <div class="movimiento-fecha">2023-10-15</div>
            <div class="movimiento-descripcion">Día de vacaciones</div>
            <div class="movimiento-dias">-1 día</div>
        </div>
    `;
}

// Función para mostrar los botones de manejo de empleados
function mostrarBotones() {
    const botones = document.querySelector('.botones_manejo_empleados');
    botones.classList.add('mostrar');
}

// Función para mostrar el modal de agregar empleado
function mostrarModalAgregarEmpleado() {
    const modal = document.getElementById('modal_agregar_empleado');
    modal.classList.add('mostrar');
    document.body.style.overflow = 'hidden'; // Deshabilitar scroll
}

// Función para mostrar el modal de modificar empleado
function mostrarModalModificarEmpleado() {
    console.log('[DEBUG] Mostrando modal de modificación de empleado');
    const modal = document.getElementById('modal_modificar_empleado');
    const select = document.getElementById('empleado_a_modificar');
    
    if (!modal || !select) {
        console.error('No se encontró el modal o el select de modificación');
        return;
    }
    
    // Limpiar opciones existentes
    select.innerHTML = '<option value="" disabled selected>Seleccione un empleado</option>';
    
    // Cargar empleados en el select

    empleados_modificar = [];

    fetch('/obtener-empleados')
        .then(response => response.json())
        .then(data => {
            empleados_modificar = data.empleados;
            data.empleados.forEach(empleado => {
                const option = document.createElement('option');
                option.value = empleado.id_empleado;
                option.textContent = `${empleado.nombre} - ${empleado.documento_identidad} - ${empleado.puesto}`;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al cargar empleados:', error);
            alert('Error al cargar la lista de empleados');
        });
    
    modal.classList.add('mostrar');
    document.body.style.overflow = 'hidden';
    
    // Cargar puestos en el select
    cargarPuestos('puesto_modificar');
    
    // Cargar datos del empleado cuando se selecciona uno
    select.addEventListener('change', async function() {
        const empleadoId = this.value;
        if (!empleadoId) return;
        
        const empleado = empleados_modificar.find(empleado => empleado.id_empleado == empleadoId);
        if (!empleado) return;
        
        // Llenar los campos del formulario con los datos del empleado
        document.getElementById('nombre_modificar').value = empleado.nombre || '';
        document.getElementById('documento_modificar').value = empleado.documento_identidad || '';
        document.getElementById('puesto_modificar').value = empleado.id_puesto || '';
        
        // Establecer el valor del select de puestos
        const puestoSelect = document.getElementById('puesto_modificar');
        if (puestoSelect) {
            // Buscar la opción que coincida con el ID del puesto del empleado
            for (let i = 0; i < puestoSelect.options.length; i++) {
                if (puestoSelect.options[i].value == empleado.id_puesto) {
                    puestoSelect.selectedIndex = i;
                    break;
                }
            }
        }
    });
    
    // Cerrar el modal al hacer clic en el botón de cancelar
    const cancelarBtn = document.getElementById('cancelar_modificar_btn');
    if (cancelarBtn) {
        cancelarBtn.onclick = function() {
            modal.classList.remove('mostrar');
            document.body.style.overflow = 'auto';
        };
    }
    
    // Cerrar el modal al hacer clic fuera del contenido
    modal.onclick = function(event) {
        if (event.target === modal) {
            modal.classList.remove('mostrar');
            document.body.style.overflow = 'auto';
        }
    };
}

// Función para mostrar el modal de eliminar empleado
function mostrarModalEliminarEmpleado() {
    const modal = document.getElementById('modal_eliminar_empleado');
    const select = document.getElementById('empleado_a_eliminar');
    
    // Limpiar opciones existentes
    select.innerHTML = '<option value="" disabled selected>Seleccione un empleado</option>';
    
    // Cargar empleados en el select
    fetch('/obtener-empleados')
        .then(response => response.json())
        .then(data => {
            data.empleados.forEach(empleado => {

                const option = document.createElement('option');
                option.value = empleado.id_empleado;
                option.textContent = `${empleado.nombre} - ${empleado.documento_identidad} - ${empleado.puesto}`;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al cargar empleados:', error);
            alert('Error al cargar la lista de empleados');
        });
    
    modal.classList.add('mostrar');
    document.body.style.overflow = 'hidden'; // Deshabilitar scroll
}

// Función para manejar la eliminación de empleado
function manejarEliminarEmpleado(event) {
    // Prevenir el comportamiento por defecto del formulario
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    const empleadoSelect = document.getElementById('empleado_a_eliminar');
    if (!empleadoSelect) {
        console.error('No se encontró el elemento empleado_a_eliminar');
        return;
    }
    
    const empleadoId = empleadoSelect.value;
    console.log('Intentando eliminar empleado con ID:', empleadoId);
    
    if (!empleadoId) {
        alert('Por favor seleccione un empleado');
        return;
    }
    
    if (!confirm('¿Está seguro de eliminar este empleado? Esta acción no se puede deshacer.')) {
        return;
    }
    
    console.log(`Enviando solicitud DELETE a /eliminar-empleado/${empleadoId}`);
    
    fetch(`/eliminar-empleado/${empleadoId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        console.log('Respuesta recibida:', response);
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || 'Error al eliminar el empleado');
            }).catch(() => {
                throw new Error(`Error HTTP ${response.status}`);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Datos de respuesta:', data);
        if (data && data.success) {
            alert('Empleado eliminado correctamente');
            cerrarModal();
            // Recargar la lista de empleados
            limpiarTablaEmpleados();
            cargarEmpleados().catch(err => {
                console.error('Error al recargar empleados:', err);
            });
        } else {
            throw new Error(data ? data.message : 'Respuesta inválida del servidor');
        }
    })
    .catch(error => {
        console.error('Error en la solicitud:', error);
        alert('Error al eliminar el empleado: ' + (error.message || 'Error desconocido'));
    });
}

// Función para cerrar cualquier modal
function cerrarModal() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('mostrar');
    });
    document.body.style.overflow = 'auto'; // Restaurar scroll
}

// Función para limpiar la tabla de empleados
function limpiarTablaEmpleados() {
    const contenedorFilas = document.getElementById('contenedor_filas_empleados');
    contenedorFilas.innerHTML = '';
}

function manejarAgregarEmpleado(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const empleado = {
        nombre: formData.get('nombre'),
        documento_identidad: formData.get('documento_identidad'),
        activo: formData.get('activo') === 'on',
        fecha_contratacion: formData.get('fecha_contratacion'),
        puesto: formData.get('puesto')
    };
    
    console.log('Verificando empleado:', empleado);
    
    // Primero verificar si el empleado ya existe
    fetch('/verificar-empleado', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            documento_identidad: empleado.documento_identidad,
            nombre: empleado.nombre
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Si la verificación es exitosa, proceder a agregar el empleado
            console.log('Empleado verificado, procediendo a agregar...');
            return fetch('/agregar-empleado', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(empleado)
            });
        } else {
            // Mostrar mensaje de error específico
            throw new Error(data.message || 'Error al verificar el empleado');
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al agregar el empleado');
        }
        return response.json();
    })
    .then(data => {
        console.log('Empleado agregado:', data);
        
        // Cerrar el modal y limpiar el formulario
        cerrarModal();
        event.target.reset();
        
        // Recargar la lista de empleados después de un breve retraso
        setTimeout(() => {
            limpiarTablaEmpleados();
            cargarEmpleados().then(() => {
                console.log('Empleados recargados exitosamente');
            }).catch(error => {
                console.error('Error al recargar empleados:', error);
            });
        }, 500);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al agregar el empleado: ' + error.message);
    });
}

function manejarEliminarEmpleado(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const empleado_id = formData.get('empleado_id');
    
    console.log('Eliminando empleado con ID:', empleado_id);
    
    fetch('/eliminar-empleado/' + empleado_id, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al eliminar el empleado');
        }
        return response.json();
    })
    .then(data => {
        console.log('Empleado eliminado:', data);
        
        // Cerrar el modal y limpiar el formulario
        cerrarModal();
        event.target.reset();
        
        // Recargar la lista de empleados después de un breve retraso
        setTimeout(() => {
            limpiarTablaEmpleados();
            cargarEmpleados().then(() => {
                console.log('Empleados recargados exitosamente');
            }).catch(error => {
                console.error('Error al recargar empleados:', error);
            });
        }, 500);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar el empleado: ' + error.message);
    });
}

function manejarModificarEmpleado(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const empleado_id = document.getElementById('empleado_a_modificar').value;
    
    console.log('Datos del formulario:', {
        empleado_id: empleado_id,
        nombre: formData.get('nombre'),
        documento: formData.get('documento'),
        puesto: formData.get('puesto')
    });
    
    fetch('/modificar-empleado/' + empleado_id, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            valor_documento_identidad: formData.get('documento'),
            nombre: formData.get('nombre'),
            id_puesto: formData.get('puesto')
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al modificar el empleado');
        }
        return response.json();
    })
    .then(data => {
        console.log('Empleado modificado:', data);
        
        // Cerrar el modal y limpiar el formulario
        cerrarModal();
        event.target.reset();
        
        // Recargar la lista de empleados después de un breve retraso
        setTimeout(() => {
            limpiarTablaEmpleados();
            cargarEmpleados().then(() => {
                console.log('Empleados recargados exitosamente');
            }).catch(error => {
                console.error('Error al recargar empleados:', error);
            });
        }, 500);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al modificar el empleado: ' + error.message);
    });
}

// ----------------------------------------------------- //
// Eventos de carga de empleados y puestos
document.addEventListener('DOMContentLoaded', function() {
    const contenedor = document.getElementById('contenedor_filas_empleados');
    
    // Cargar puestos cuando el DOM esté listo
    cargarPuestos();
    
    // También cargar puestos cuando se muestre el modal de agregar empleado
    document.addEventListener('click', function(e) {
        if (e.target && e.target.id === 'agregar_empleado_btn') {
            // Pequeño retraso para asegurar que el modal esté visible
            setTimeout(cargarPuestos, 100);
        }
    });
    const urlParams = new URLSearchParams(window.location.search);
    const fromLogin = urlParams.get(AUTH_PARAM) === 'true';

    console.log("Estado de autenticación:", { fromLogin });

    // Si el contenedor existe y viene de un login exitoso:
    if (contenedor && fromLogin) {
        // Limpiar el parámetro de la URL sin recargar la página
        const newUrl = window.location.pathname;
        window.history.replaceState({}, document.title, newUrl);
        
        // -------------------------------------------------- //
        // Cargar los empleados y mostrar los botones
        cargarEmpleados();
        mostrarBotones();
    }

    // Evento para el botón de ver movimientos
    const verMovimientosBtn = document.getElementById('ver_movimientos');
    if (verMovimientosBtn) {
        verMovimientosBtn.addEventListener('click', mostrarModalMovimientos);
    }

    // Cerrar con la tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            cerrarModal();
        }
    });
});

// ----------------------------------------------------- //
// Eventos de gestión de empleados (Agregar, Eliminar, Modificar)
document.addEventListener('DOMContentLoaded', function() {
    // ----------------------------------------------------- //
    // Elementos del DOM
    const btn_agregar = document.getElementById('agregar_empleado');
    const form_agregar = document.getElementById('agregar_empleado_form');
    const btn_eliminar = document.getElementById('eliminar_empleado');
    const form_eliminar = document.getElementById('eliminar_empleado_form');
    const btn_modificar = document.getElementById('modificar_empleado');
    const form_modificar = document.getElementById('modificar_empleado_form');
    
    // Evento para abrir el modal de agregar empleado
    if (btn_agregar) {
        btn_agregar.addEventListener('click', mostrarModalAgregarEmpleado);
    }
    
    // Evento para manejar el envío del formulario de agregar
    if (form_agregar) {
        form_agregar.addEventListener('submit', manejarAgregarEmpleado);
    }
    
    // Evento para abrir el modal de eliminar empleado
    if (btn_eliminar) {
        btn_eliminar.addEventListener('click', mostrarModalEliminarEmpleado);
    }
    
    // Evento para manejar el envío del formulario de eliminar
    if (form_eliminar) {
        form_eliminar.addEventListener('submit', manejarEliminarEmpleado);
    }
    
    // Evento para abrir el modal de modificar empleado
    if (btn_modificar) {
        btn_modificar.addEventListener('click', mostrarModalModificarEmpleado);
    }
    
    // Evento para el formulario de modificar empleado
    const modificarForm = document.getElementById('modificar_empleado_form');
    if (modificarForm) {
        modificarForm.addEventListener('submit', manejarModificarEmpleado);
    }
    
    // Cerrar modales con los botones de cancelar
    function setupCancelButtons() {
        // Botón de cancelar en el modal de agregar
        const cancelarAgregarBtn = document.getElementById('cancelar_agregar_btn');
        if (cancelarAgregarBtn) {
            cancelarAgregarBtn.addEventListener('click', function(e) {
                e.preventDefault();
                cerrarModal();
            });
        }

        // Botón de cancelar en el modal de eliminar
        const cancelarEliminarBtn = document.getElementById('cancelar_eliminar_btn');
        if (cancelarEliminarBtn) {
            cancelarEliminarBtn.addEventListener('click', function(e) {
                e.preventDefault();
                cerrarModal();
            });
        }

        // Botón de cancelar en el modal de modificar
        const cancelarModificarBtn = document.getElementById('cancelar_modificar_btn');
        if (cancelarModificarBtn) {
            cancelarModificarBtn.addEventListener('click', function(e) {
                e.preventDefault();
                cerrarModal();
            });
        }
    }
    
    // Configurar los botones de cancelar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupCancelButtons);
    } else {
        setupCancelButtons();
    }
    
    // 2. Al hacer clic fuera del contenido
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                cerrarModal();
            }
        });
    });
});
