jQuery.noConflict();

(function($) {
    jQuery(document).ready(function() {
        jQuery('#detalledeventa_set-group').change(function(){
            calcular_subtotal();
            obtener_precio();
        });

        jQuery('form input[type=submit]').click(function(e) {
            guardar();
        });
    });
})(django.jQuery);

function calcular_subtotal() {
    subtotal = 0;
    var rows = jQuery("tr[id*='detalledeventa_set']");
    var rows_length = rows.length -1; // para evadir el empty
    for( var i=0; i<rows_length; i++){
        var cantidad = document.getElementById('id_detalledeventa_set-'+i+'-cantidad').value;
        var precio = document.getElementById('id_detalledeventa_set-'+i+'-precio_unitario').value;
        jQuery("#id_detalledeventa_set-" + i + "-subtotal").val(cantidad*precio);
    }
    calcular_total();
}


function calcular_total() {
    total = 0;
    var rows = jQuery("tr[id*='detalledeventa_set']");
    var rows_length = rows.length -1;

    for(var i=0 ; i<rows_length ; i++){
        var subtotal = document.getElementById('id_detalledeventa_set-'+i+'-subtotal');
        if(subtotal.value != ''){
        total += parseInt(unformat(subtotal));
       }
    }
    jQuery('#id_total').val(separarMiles(total));
}

function obtener_precio() {
    var rows = jQuery("tr[id*='detalledeventa_set']");
    var rows_length = rows.length -1;
    for( var i=0; i<rows_length; i++){
        var producto = document.getElementById('id_detalledeventa_set-'+i+'-producto').value;
        var indice = i;
        jQuery.ajax({
                data : {'producto_id' : producto, 'cliente_id': document.getElementById('id_cliente').value},
                url : "/admin/productos/getproducto/",
                type : "get",
                success : function(data){
                   jQuery("#id_detalledeventa_set-" + indice.toString() + "-precio_unitario").val(data.precio);
                   calcular_subtotal();
                }
            });
    }
}

function unformat(input){
		return input.value.replace(/\./g,'').replace(',','.');
}

function separarMiles(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function guardar() {
    jQuery('.auto').each(function (){
        jQuery(this).val((jQuery(this).val()!='')?unformat(document.getElementById(this.id.toString())):'');
    });
}