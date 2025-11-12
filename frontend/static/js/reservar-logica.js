$(document).ready(function() {
    // Estas variables (pricePerNight y reservedDates) se asumen definidas
    // en el HTML antes de que este script se cargue.
    
    var checkInDate, checkOutDate;

    function calculateTotal(checkIn, checkOut) {
        var d_in = new Date(checkIn);
        var d_out = new Date(checkOut);
        
        if (d_in && d_out && d_out > d_in) {
            var nights = Math.ceil((d_out - d_in) / (1000 * 60 * 60 * 24));
            // pricePerNight se usa como variable global
            var total = nights * pricePerNight; 
            $('#total').text('$' + total + ' (' + nights + ' noches)');
            return true;
        } else {
            $('#total').text('$0');
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
        var calendarEl = document.getElementById('calendar');
        if (calendarEl && calendarEl.fullCalendar) {
            calendarEl.fullCalendar('unselect');
        }
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
            resetForm();

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
            resetForm();
        }
    });

    calendar.render();
    
    $('#guests').on('change', function() {
        if ($('#check_in_hidden').val() && $('#check_out_hidden').val()) {
            calculateTotal($('#check_in_hidden').val(), $('#check_out_hidden').val());
        }
    });
});