const formularioCarrito = document.getElementById('formularioCarrito');
const cantidadInput = document.getElementById('cantidad');


formularioCarrito.addEventListener('submit', function (event) {
    event.preventDefault();


    const cantidad = cantidadInput.value;

    if (cantidad && cantidad > 0) {

        const mensaje = `Hola, me gustaría comprar ${cantidad} helados caseros.`;


        const numeroWhatsApp = "+573016233107";


        const enlaceWhatsApp = `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(mensaje)}`;

        window.location.href = enlaceWhatsApp;
    } else {
        alert("Por favor, ingresa una cantidad válida.");
    }
});
