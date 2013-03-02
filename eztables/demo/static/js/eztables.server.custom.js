(function($, Django, Demo){

    "use strict";

    var $table = $('#browser-table');

    function fnFilterGlobal() {
        $table.dataTable().fnFilter(
            $("#global-filter").val(),
            null,
            false,
            false
        );
    }

    function fnFilterColumn(i) {
        $table.dataTable().fnFilter(
            $("#filter-"+i).val(),
            i,
            false,
            false
        );
    }

    function createFilter(i) {
        return function() { fnFilterColumn(i); };
    }

    $(function(){
        $table.dataTable({
            "bPaginate": true,
            "sPaginationType": "bootstrap",
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": Django.url('DT-browsers-custom'),
            "fnRowCallback": Demo.colorRow
        });

        $("#global-filter").keyup( fnFilterGlobal );
        $("#global-regex").click( fnFilterGlobal );

        for (var i=0; i<6; i++) {
            $("#filter-"+i).keyup(createFilter(i));
            $("#regex-"+i).click(createFilter(i));
        }

    });


}(window.jQuery, window.Django, window.Demo));
