(function($, Django, Demo){

    "use strict";

    /**
     * Render "name version" as name column
     */
    var render_name = function(data, type, row) {
        var name = data;
        if (row.version) {
            name += ' ' + row.version;
        }
        return name;
    };

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
                { "mData": "name", 'mRender': render_name },
                { "mData": "platform" },
                { "mData": "engine_version" },
                { "mData": "css_grade" }
            ]
        });
    });


}(window.jQuery, window.Django, window.Demo));
