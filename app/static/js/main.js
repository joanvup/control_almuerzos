$(document).ready(function() {

    // --- Lógica del Reloj en la página de registro ---
    // static/js/main.js

    function actualizarReloj() {
        if ($('#fecha-actual').length && $('#hora-actual').length) {
            const now = new Date();
        
            // --- Lógica para la Fecha (sin cambios) ---
            const opcionesFecha = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            const fechaFormateada = now.toLocaleDateString('es-ES', opcionesFecha);
            $('#fecha-actual').text(fechaFormateada.charAt(0).toUpperCase() + fechaFormateada.slice(1));

            // --- Nueva Lógica para la Hora en formato hh:mm:ss AM/PM ---
            let hours = now.getHours();
            let minutes = now.getMinutes();
            let seconds = now.getSeconds();

            // 1. Determinar si es AM o PM
            const ampm = hours >= 12 ? 'PM' : 'AM';

            // 2. Convertir la hora de formato 24h a 12h
            hours = hours % 12;
            hours = hours ? hours : 12; // La hora '0' (medianoche) debe ser '12'

            // 3. Añadir un cero delante a los minutos y segundos si son menores de 10
            const paddedMinutes = String(minutes).padStart(2, '0');
            const paddedSeconds = String(seconds).padStart(2, '0');
            const paddedHours = String(hours).padStart(2, '0'); // También a las horas para mantener el formato hh

            // 4. Construir la cadena de texto final
            const horaFormateada = `${paddedHours}:${paddedMinutes}:${paddedSeconds} ${ampm}`;

            $('#hora-actual').text(horaFormateada);
        }
    }
    actualizarReloj();
    setInterval(actualizarReloj, 1000);


    // --- Lógica de Registro de Almuerzo con AJAX (Fetch API) ---
    $('#registro-form').on('submit', function(e) {
        e.preventDefault();
        const input = $('#id_persona_input');
        const idPersona = input.val();

        if (idPersona.trim() === '') return;

        fetch('/procesar_registro', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `id_persona=${idPersona}`
        })
        .then(response => response.json())
        .then(data => {
            const mensajeDiv = $('#mensaje-registro');
            if (data.success) {
                mensajeDiv.html(`<div class="alert alert-success">${data.registro.nombre_persona}: ${data.message}</div>`);
                // === INICIO DE CAMBIOS ===
                // Construir el botón de eliminar SÓLO si el usuario es admin
                let deleteButtonHtml = '';
                if (typeof IS_ADMIN !== 'undefined' && IS_ADMIN) {
                    deleteButtonHtml = `
                        <form action="/registro/delete/${data.registro.id_registro}" method="POST" class="d-inline" onsubmit="return confirm('¿Estás seguro de que quieres eliminar este registro? Es una acción irreversible.');">
                            <button type="submit" class="btn btn-sm btn-outline-danger" title="Eliminar Registro">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </form>
                    `;
                }

                // Añadir a la tabla
                const newRow = `
                    <tr>
                        <td>${new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</td>
                        <td>${data.registro.id_persona}</td>
                        <td>${data.registro.nombre_persona}</td>
                        <td>${data.registro.dpto}</td>
                        <td>${data.registro.tipo_control}</td>
                        <td>
                            <a href="/imprimir_ticket/${data.registro.id_registro}" target="_blank" class="btn btn-sm btn-outline-secondary" title="Reimprimir Ticket">
                                <i class="fas fa-print"></i>
                            </a>
                            ${deleteButtonHtml}
                        </td>
                    </tr>`;
                // === FIN DE CAMBIOS ===
                
                $('#tabla-registros-body').prepend(newRow);
                $('#no-registros-row').hide(); // Ocultar mensaje de "no hay registros"
                
                // Imprimir ticket si está habilitado
                if (data.registro.imprime_ticket) {
                    window.open(`/imprimir_ticket/${data.registro.id_registro}`, '_blank');
                }

            } else {
                mensajeDiv.html(`<div class="alert alert-danger">${data.message}</div>`);
            }
            input.val('').focus(); // Limpiar y enfocar el input
            setTimeout(() => mensajeDiv.empty(), 4000); // Borrar mensaje después de 4 segundos
        })
        .catch(error => console.error('Error:', error));
    });


    // --- Lógica para Modales CRUD (Dptos, Tipos, etc.) ---
    $('.edit-btn').on('click', function() {
        const modalId = $(this).data('bs-target');
        const modal = $(modalId);
        const form = modal.find('form');
        
        const id = $(this).data('id');
        const nombre = $(this).data('nombre');
        
        form.find('input[name*="id_"]').val(id); // Busca cualquier input que contenga "id_"
        form.find('input[name*="nombre_"]').val(nombre); // Busca cualquier input que contenga "nombre_"
        
        modal.find('.modal-title').text('Editar ' + modal.find('label').first().text().replace('Nombre del ',''));
    });

    $('#btn-nuevo-dpto, #btn-nuevo-tipopersona, #btn-nuevo-tipocontrol').on('click', function() {
        const modalId = $(this).data('bs-target');
        const modal = $(modalId);
        const form = modal.find('form');
        
        form[0].reset(); // Limpia el formulario
        form.find('input[name*="id_"]').val('');
        modal.find('.modal-title').text('Nuevo ' + modal.find('label').first().text().replace('Nombre del ',''));
    });


    // --- Lógica del selector de reportes ---
    $('#tipo_reporte').on('change', function() {
        const selectedType = $(this).val();
        $('.filter-group').hide();
        $('.filter-group select').prop('disabled', true);

        if (['persona', 'tipo_control', 'dpto', 'tipo_persona'].includes(selectedType)) {
            const filterDiv = $(`#filtro-${selectedType}`);
            filterDiv.show();
            filterDiv.find('select').prop('disabled', false);
        }
        
        // Deshabilitar fecha_fin para reporte de día
        if (selectedType === 'dia') {
             $('#fecha_fin').prop('disabled', true);
        } else {
             $('#fecha_fin').prop('disabled', false);
        }
    }).trigger('change'); // Ejecutar al cargar la página

    // --- Lógica para el Modal de Usuarios ---
    $('#btn-nuevo-usuario').on('click', function() {
        const modal = $('#usuarioModal');
        const form = modal.find('form');

        form[0].reset(); // Limpia el formulario
        $('#form-id-usuario').val(''); // Asegura que el ID oculto esté vacío
        modal.find('.modal-title').text('Nuevo Usuario');
        // Para nuevos usuarios, la contraseña es requerida
        $('#form-password').prop('required', true);
        $('#form-confirm-password').prop('required', true);
    });

    $('.edit-btn-usuario').on('click', function() {
        const modal = $('#usuarioModal');
        const form = modal.find('form');

        const id = $(this).data('id');
        const username = $(this).data('username');
        const rolId = $(this).data('rol-id');

        $('#form-id-usuario').val(id);
        $('#form-username').val(username);
        $('#form-rol').val(rolId);
    
        // Limpiar campos de contraseña por seguridad
        $('#form-password').val('');
        $('#form-confirm-password').val('');
    
        // Para editar, la contraseña no es requerida
        $('#form-password').prop('required', false);
        $('#form-confirm-password').prop('required', false);

        modal.find('.modal-title').text('Editar Usuario: ' + username);
    });

});