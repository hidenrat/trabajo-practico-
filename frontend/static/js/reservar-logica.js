$(document).ready(function() {
    // Estas variables (pricePerNight y reservedDates) se asumen definidas
    // en el HTML antes de que este script se cargue.
    
    var checkInDate, checkOutDate;
    // Cuando el calendario dispara `unselect`, por defecto no queremos
    // limpiar el formulario — queremos que la selección persista hasta
    // que el usuario seleccione otro rango o ocurra un solapamiento.
    // Usamos esta bandera para indicar cuándo `unselect` debe limpiar.
    var clearOnUnselect = false;

    function calculateTotal(checkIn, checkOut) {
        var d_in = new Date(checkIn);
        var d_out = new Date(checkOut);
        
        if (d_in && d_out && d_out > d_in) {
            var nights = Math.ceil((d_out - d_in) / (1000 * 60 * 60 * 24));
            // pricePerNight se usa como variable global
            var total = nights * pricePerNight; 
            $('#total').text('$' + total + ' (' + nights + ' noches)');
            $('#input-total').val(total);
            return true;
        } else {
            $('#total').text('$0');
            $('#input-total').val(0);
            return false;
        }
    }
    
    function resetForm() {
        $('#check_in_hidden').val('');
        $('#check_out_hidden').val('');
        $('#check_in_display').text('--');
        $('#check_out_display').text('--');
        $('#submit-button').prop('disabled', true);
        $('#error-message').hide().text('');
        $('#total').text('$0');
    }

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        selectable: true,
        events: reservedDates, 
        dayMaxEvents: true,
        
        selectAllow: function(selectInfo) {
            var today = new Date();
            today.setHours(0, 0, 0, 0); 
            return selectInfo.start >= today; 
        },
        
        eventContent: function(arg) {
            if (arg.event.classNames.includes('reserved-event')) {
                let textEl = document.createElement('span');
                textEl.classList.add('reserved-text');
                textEl.innerText = arg.event.title; 
                return { domNodes: [textEl] };
            }
        },

        select: function(info) {
            // No limpiamos el formulario entero aquí para evitar que un
            // siguiente click lo borre; solo ocultamos errores previos.
            $('#error-message').hide().text('');

            // Marcamos que, por defecto, al deseleccionar NO se debe limpiar.
            clearOnUnselect = false;

            var rangeStart = info.startStr;
            var rangeEnd_FC = info.end; 
            var rangeEnd_Checkout = new Date(rangeEnd_FC);
            rangeEnd_Checkout.setDate(rangeEnd_Checkout.getDate() - 1); 
            var rangeEnd = rangeEnd_Checkout.toISOString().slice(0, 10);

            var isOverlapping = false;
            reservedDates.forEach(function(event) {
                var eventStart = new Date(event.start);
                var eventEnd = new Date(event.end);
                
                if (info.start < eventEnd && info.end > eventStart) {
                    isOverlapping = true;
                }
            });

            if (isOverlapping) {
                $('#error-message').text('🚫 La selección se solapa con una reserva existente.').show();
                // Queremos que en este caso la deselección LIMPIE el formulario,
                // así que activamos la bandera y llamamos a unselect.
                clearOnUnselect = true;
                calendar.unselect();
                return;
            }
            
            // Si la selección es válida
            checkInDate = rangeStart;
            checkOutDate = rangeEnd;
            
            // Muestra y guarda los datos
            $('#check_in_hidden').val(checkInDate);
            $('#check_out_hidden').val(rangeEnd);
            $('#check_in_display').text(checkInDate);
            $('#check_out_display').text(rangeEnd);
            $('#submit-button').prop('disabled', false);

            calculateTotal(checkInDate, rangeEnd);
        },

        unselect: function() {
            // Solo limpiar si algo pidió explícitamente la limpieza.
            if (clearOnUnselect) {
                resetForm();
                clearOnUnselect = false;
            }
            // Si clearOnUnselect es false, mantenemos la selección y el formulario.
        }
    });

    calendar.render();
    
    // Maneja el botón de cancelar selección: deselecciona el calendario
    // y limpia el formulario. Usamos la bandera `clearOnUnselect` para
    // permitir que el handler `unselect` realice la limpieza sin provocar
    // recursión accidental.
    $('#cancel-selection').on('click', function() {
        clearOnUnselect = true;
        // Llamamos a la API de FullCalendar v5 para deseleccionar.
        if (typeof calendar !== 'undefined' && calendar) {
            calendar.unselect();
        } else {
            // Por seguridad, si no hay calendario aún, limpiamos directamente.
            resetForm();
            clearOnUnselect = false;
        }
    });

    $('#guests').on('change', function() {
        if ($('#check_in_hidden').val() && $('#check_out_hidden').val()) {
            calculateTotal($('#check_in_hidden').val(), $('#check_out_hidden').val());
        }
    });
});