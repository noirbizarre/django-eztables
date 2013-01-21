(function($, Django){

    "use strict";


    $(function(){
        $('#browser-table').dataTable({
            "bPaginate": true,
            "sPaginationType": "bootstrap",
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": Django.url('browsers-datatables')
        });
    });

}(window.jQuery, window.Django));
