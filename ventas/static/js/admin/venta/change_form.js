(function($) {
    $(document).ready(function() {
        $('select').change(function(){
            vector = $(this).attr("id").split("-");
            if(vector[0] === "id_detalledeventa_set"){
                var optionSelected = $(this).find("option:selected");
                var valueSelected  = optionSelected.val();
                if(!valueSelected){
                    $("#id_detalledeventa_set-" + vector[1] + "-precio_unitario").val("0");
                    return
                }
                $.ajax({
                    data : {'producto_id' : valueSelected, 'cliente_id': document.getElementById('id_cliente').value},
                    url : "/admin/productos/getproducto/",
                    type : "get",
                    success : function(data){
                        $("#id_detalledeventa_set-" + vector[1] + "-precio_unitario").val(separarMiles(data.precio));
                        var cantidad = document.getElementById('id_detalledeventa_set-' + vector[1] + '-cantidad').value;
                        var precio = data.precio;
                        $("#id_detalledeventa_set-" + vector[1] + "-subtotal").val(separarMiles(cantidad*precio));
                        calcular_total();
                    }
                });
            }
        });

        $('#detalledeventa_set-group').change(function(e){
            var element_id = e.target.id;
            if (element_id.includes('cantidad')){
                vector = element_id.split("-");
                calcular_subtotal(vector[1]);

            }
        });

        $('form input[type=submit]').click(function(e) {
            guardar();
        });
    });
})(jQuery);

function calcular_subtotal(element_id) {
    let cantidad_element = document.getElementById('id_detalledeventa_set-' + element_id + '-cantidad');
    let precio_element = document.getElementById('id_detalledeventa_set-' + element_id + '-precio_unitario');
    let cantidad_int = parseInt(unformat(cantidad_element));
    let precio_int = parseInt(unformat(precio_element));

    $("#id_detalledeventa_set-" + element_id + "-subtotal").val(separarMiles(cantidad_int*precio_int));
    calcular_total();
}


function calcular_total() {
    total = 0;
    var rows = $("tr[id*='detalledeventa_set']");
    var rows_length = rows.length -1;

    for(var i=0 ; i<rows_length ; i++){
        var subtotal = document.getElementById('id_detalledeventa_set-'+i+'-subtotal');
        if(subtotal.value != ''){
        total += parseInt(unformat(subtotal));
       }
    }
    $('#id_total').val(separarMiles(total));
}

function obtener_precio() {
    var rows = $("tr[id*='detalledeventa_set']");
    var rows_length = rows.length -1;
    for( var i=0; i<rows_length; i++){
        var producto = document.getElementById('id_detalledeventa_set-'+i+'-producto').value;
        var indice = i;
        $.ajax({
                data : {'producto_id' : producto, 'cliente_id': document.getElementById('id_cliente').value},
                url : "/admin/productos/getproducto/",
                type : "get",
                success : function(data){
                   $("#id_detalledeventa_set-" + indice.toString() + "-precio_unitario").val(data.precio);
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
    $('.auto').each(function (){
        $(this).val(($(this).val()!='')?unformat(document.getElementById(this.id.toString())):'');
    });
}