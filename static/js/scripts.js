
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
            fila.innerHTML = `
                <div class="empleado_id">${empleado.id}</div>
                <div class="empleado_nombre">${empleado.nombre}</div>
                <div class="empleado_vacaciones_restantes">${empleado.vacaciones_restantes}</div>
            `;
            contenedorFilas.appendChild(fila);
        });
        
        // console.log("Empleados cargados:", empleados);
    
    } catch (error) {
        console.error('Error al cargar empleados:', error);
        contenedorFilas.innerHTML = '<div class="error">Error al cargar los empleados. Intente nuevamente.</div>';
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
    const modal = document.getElementById('modalMovimientos');
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

// Función para cerrar cualquier modal
function cerrarModal() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('mostrar');
    });
    document.body.style.overflow = 'auto'; // Restaurar scroll
}

// Función para mostrar el modal de agregar empleado
function mostrarModalAgregarEmpleado() {
    const modal = document.getElementById('modal_agregar_empleado');
    modal.classList.add('mostrar');
    document.body.style.overflow = 'hidden'; // Deshabilitar scroll
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

// Manejar el envío del formulario de agregar empleado (TODO -> Agregar la lógica para guardar el empleado en la base de datos)
function manejarAgregarEmpleado(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);  // Obtiene los datos del formulario 
    const empleado = {
        nombre: formData.get('nombre'),
        vacaciones_restantes: parseInt(formData.get('vacaciones_restantes'))
    };

    // TODO -> Agregar la lógica para guardar el empleado en la base de datos
    console.log('Nuevo empleado:', empleado);
    
    // Cerrar el modal y limpiar el formulario
    cerrarModal();
    event.target.reset();
    
    // Recargar la lista de empleados
    limpiarTablaEmpleados();
    cargarEmpleados();
}

// ----------------------------------------------------- //
// Eventos de carga de empleados
document.addEventListener('DOMContentLoaded', function() {
    const contenedor = document.getElementById('contenedor_filas_empleados');
    const urlParams = new URLSearchParams(window.location.search);
    const fromLogin = urlParams.get(AUTH_PARAM) === 'true';

    // console.log("Estado de autenticación:", { fromLogin });

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
// Eventos de gestión de empleados
document.addEventListener('DOMContentLoaded', function() {

    // ----------------------------------------------------- //
    // Elementos del DOM
    const btn_agregar = document.getElementById('agregar_empleado');
    const form_agregar = document.getElementById('agregar_empleado_form');
    
    // Evento para abrir el modal de agregar empleado
    if (btn_agregar) {
        btn_agregar.addEventListener('click', mostrarModalAgregarEmpleado);
    }
    
    // Evento para manejar el envío del formulario
    if (form_agregar) {
        form_agregar.addEventListener('submit', manejarAgregarEmpleado);
    }
    
    // ----------------------------------------------------- //
    // Cerrar modales
    // 1. Al hacer clic en la X o botón de cancelar
    const cerrar_modal_btn = document.getElementById('cerrar_modal_btn');
    const cancelar_btn = document.getElementById('cancelar_btn');
    
    if (cerrar_modal_btn) {
        cerrar_modal_btn.addEventListener('click', function(e) {
            e.preventDefault();  // Evitar que se actualice la página
            e.stopPropagation();  // Evitar que el evento se propague
            console.log('Cerrando modal desde: X');
            cerrarModal();
        });
    }
    
    if (cancelar_btn) {
        cancelar_btn.addEventListener('click', function(e) {
            e.preventDefault();  // Evitar que se actualice la página
            e.stopPropagation(); 
            console.log('Cerrando modal desde: Cancelar');
            cerrarModal();
        });
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
