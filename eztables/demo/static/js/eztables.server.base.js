(function($, Django){

    "use strict";

    var Column = {
        ENGINE: 0,
        BROWSER: 1,
        PLATFORM: 2,
        ENGINE_VERSION: 3,
        GRADE: 4
    };


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
