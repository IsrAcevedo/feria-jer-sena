const formularioCarrito = document.getElementById('formularioCarrito');
const cantidadInput = document.getElementById('cantidad');


formularioCarrito.addEventListener('submit', function (event) {
    event.preventDefault();

    const cantidad = cantidadInput.value;

    if (cantidad && cantidad > 0) {
        const empresa = formularioCarrito.getAttribute('data-empresa')
        const precio = 0
        const mensaje = `
        *FACTURA DE COMPRA*
        *Empresa:* _${empresa}_

        *DETALLE FACTURA*
        *Cantidad:* _${cantidad}_
        *precio unit:* _$${precio}_
        *TOTAL A PAGAR:* _$${(cantidad * precio).toFixed(2)}_

        Gracias por tu compra!!!

        _Esta es una copia de la factura._
        _No la edites antes de enviarla._
        `;

        const numeroWhatsApp = formularioCarrito.getAttribute('data-contacto')

        const enlaceWhatsApp = `https://wa.me/+57${numeroWhatsApp}?text=${encodeURIComponent(mensaje)}`;

        window.location.href = enlaceWhatsApp;
    } else {
        alert("Por favor, ingresa una cantidad válida.");
    }
});
