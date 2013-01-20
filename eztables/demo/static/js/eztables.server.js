(function($, Django){

    "use strict";

    /**
     * Handle Server-side top navbar affix.
     */
    $(function() {
        var $wrapper = $('.subnav'),
            $subnav = $(".subnav .navbar"),
            offset = $wrapper.position();

        offset.top -= $('header.navbar').height();

        $wrapper.height($subnav.height());
        $subnav.affix({
            offset: offset
        });
    });

}(window.jQuery, window.Django));
