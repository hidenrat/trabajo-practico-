/*!
=========================================================
* LeadMark Landing page
=========================================================

* Copyright: 2019 DevCRUD (https://devcrud.com)
* Licensed: (https://devcrud.com/licenses)
* Coded by www.devcrud.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// smooth scroll
$(document).ready(function(){
    $(".navbar .nav-link, .navbar-brand").on('click', function(event) {

        if (this.hash !== "") {

            event.preventDefault();

            var hash = this.hash;

            $('html, body').animate({
                scrollTop: $(hash).offset().top
            }, 700, function(){
                window.location.hash = hash;
            });
        } 
    });
});

// protfolio filters
$(window).on("load", function() {
    var t = $(".portfolio-container");
    t.isotope({
        filter: ".new",
        animationOptions: {
            duration: 750,
            easing: "linear",
            queue: !1
        }
    }), $(".filters a").click(function() {
        $(".filters .active").removeClass("active"), $(this).addClass("active");
        var i = $(this).attr("data-filter");
        return t.isotope({
            filter: i,
            animationOptions: {
                duration: 750,
                easing: "linear",
                queue: !1
            }
        }), !1
    })
})


// change header background automatically
$(document).ready(function(){
    var images = [
        'static/imgs/header1.jpg',
        'static/imgs/header2.jpg',
        'static/imgs/header3.jpg',
        'static/imgs/rincon-lunar-6.jpg'
    ];
    var index = 0;
    setInterval(function(){
        index = (index + 1) % images.length;
        $('.header').css('background-image', 'url(' + images[index] + ')');
    }, 4500); // Change image every 4.5 seconds
});

// Carrusel infinito con soporte táctil/arrastre mejorado
$(document).ready(function(){
    var carousel = $('#experiencesCarousel');
    var startX = 0;
    var currentX = 0;
    var isDragging = false;
    var threshold = 50; // Píxeles mínimos para considerar un arrastre
    
    // Prevenir el comportamiento por defecto de arrastre de imágenes
    carousel.find('img').on('dragstart', function(e) {
        e.preventDefault();
    });
    
    // Eventos de mouse
    carousel.on('mousedown', function(e) {
        isDragging = true;
        startX = e.pageX;
        currentX = e.pageX;
        carousel.css('cursor', 'grabbing');
        carousel.carousel('pause');
        e.preventDefault();
    });
    
    carousel.on('mousemove', function(e) {
        if (!isDragging) return;
        currentX = e.pageX;
        e.preventDefault();
    });
    
    carousel.on('mouseup', function(e) {
        if (!isDragging) return;
        
        var diff = startX - currentX;
        
        // Si arrastró más del threshold, cambiar de slide
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                // Arrastró hacia la izquierda - siguiente
                carousel.carousel('next');
            } else {
                // Arrastró hacia la derecha - anterior
                carousel.carousel('prev');
            }
        }
        
        isDragging = false;
        carousel.css('cursor', 'grab');
        
        // Reanudar autoplay después de 3 segundos
        setTimeout(function() {
            carousel.carousel('cycle');
        }, 2000);
    });
    
    carousel.on('mouseleave', function(e) {
        if (!isDragging) return;
        
        isDragging = false;
        carousel.css('cursor', 'grab');
        
        // Reanudar autoplay
        setTimeout(function() {
            carousel.carousel('cycle');
        }, 3000);
    });
    
    // Eventos táctiles (móviles)
    carousel.on('touchstart', function(e) {
        isDragging = true;
        startX = e.originalEvent.touches[0].pageX;
        currentX = e.originalEvent.touches[0].pageX;
        carousel.carousel('pause');
    });
    
    carousel.on('touchmove', function(e) {
        if (!isDragging) return;
        currentX = e.originalEvent.touches[0].pageX;
    });
    
    carousel.on('touchend', function(e) {
        if (!isDragging) return;
        
        var diff = startX - currentX;
        
        // Si arrastró más del threshold, cambiar de slide
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                // Arrastró hacia la izquierda - siguiente
                carousel.carousel('next');
            } else {
                // Arrastró hacia la derecha - anterior
                carousel.carousel('prev');
            }
        }
        
        isDragging = false;
        
        // Reanudar autoplay después de 3 segundos
        setTimeout(function() {
            carousel.carousel('cycle');
        }, 3000);
    });
    
    // Hacer el carrusel infinito clonando elementos
    carousel.on('slide.bs.carousel', function (e) {
        var $e = $(e.relatedTarget);
        var idx = $e.index();
        var itemsPerSlide = 1;
        var totalItems = $('.carousel-item', carousel).length;
        
        if (idx >= totalItems - itemsPerSlide) {
            var it = itemsPerSlide - (totalItems - idx);
            for (var i = 0; i < it; i++) {
                if (e.direction == "left") {
                    $('.carousel-item', carousel).eq(i).appendTo('.carousel-inner', carousel);
                } else {
                    $('.carousel-item', carousel).eq(0).appendTo('.carousel-inner', carousel);
                }
            }
        }
    });
});

