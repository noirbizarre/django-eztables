(function($, hljs){

    "use strict";

    var Column = {
        ENGINE: 0,
        BROWSER: 1,
        VERSION: 2,
        PLATFORM: 3,
        ENGINE_VERSION: 4,
        GRADE: 5
    };

    var Demo = window.Demo = {

        /**
         * Color the row given its CSS grade
         */
        colorRow: function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            // If row is an object, use the attribute name, else use the index
            var field = 'css_grade' in aData ? 'css_grade' : Column.GRADE;

            switch(aData[field]) {
                case 'A':
                    $(nRow).addClass('success');
                    break;
                case 'C':
                    $(nRow).addClass('info');
                    break;
                case 'X':
                    $(nRow).addClass('error');
                    break;
                default:
                    break;
            }
        }
    };


    $(function() {
        // Render embed code
        $('pre:not([data-url])').each(function(i, el) {
            hljs.highlightBlock(el);
        });

        // Load and render external files
        $('pre[data-url]').each(function(i, el) {
            $.get($(this).data('url'), function(data){
                $(el).text(data);
                hljs.highlightBlock(el);
            }, "text");
        });
    });

    return Demo;

}(window.jQuery, window.hljs));
