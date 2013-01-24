(function($, Django, Demo){

    "use strict";

    $(function(){
        $('#browser-table').dataTable({
            "bPaginate": true,
            "sPaginationType": "bootstrap",
            "bScrollCollapse": true,
            "fnRowCallback": Demo.colorRow
        });
    });

}(window.jQuery, window.Django, window.Demo));
