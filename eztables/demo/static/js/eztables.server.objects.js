(function($, Django, Demo){

    "use strict";

    $(function(){
        $('#browser-table').dataTable({
            "bPaginate": true,
            "sPaginationType": "bootstrap",
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": Django.url('DT-browsers-objects'),
            "fnRowCallback": Demo.colorRow,
            "aoColumns": [
                { "mData": "engine" },
                { "mData": "name" },
                { "mData": "platform" },
                { "mData": "engine_version" },
                { "mData": "css_grade" }
            ]
        });
    });


}(window.jQuery, window.Django, window.Demo));
