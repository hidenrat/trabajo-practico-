document.addEventListener('DOMContentLoaded', function() {
    const apiURL = 'http://127.0.0.1:5003/api/cabanas';
    const portfolioContainer = document.querySelector('.portfolio-container'); 

    fetch(apiURL)
        .then(response => {
            if (!response.ok) {
                //Si el servidor (5003) no responde, lanza un error
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            //Iterar sobre los datos recibidos del Backend (5003)
            data.forEach(cabana => {
                const itemHTML = `
                    <div class="col-md-6 col-lg-4 web new">
                        <div class="portfolio-item">
                            <img src="static/imgs/web-1.jpg" class="img-fluid" alt="${cabana.nombre}">
                            <div class="content-holder">
                                <div class="text-holder">
                                    <h6 class="title">${cabana.nombre}</h6>
                                    <p class="subtitle">Tipo: ${cabana.tipo} | Precio por Noche: $${cabana.precio_noche}</p>
                                </div>
                            </div>   
                        </div>             
                    </div>
                `;
                portfolioContainer.insertAdjacentHTML('beforeend', itemHTML);
            });
        })
        .catch(error => {
            console.error('No se pudieron cargar las cabañas desde la API:', error);
            //Muestra un mensaje de error al usuario si la API falla
            portfolioContainer.innerHTML = '<p class="text-center text-danger">Error al cargar la información de cabañas. Revisa el servidor 5003.</p>';
        });
});