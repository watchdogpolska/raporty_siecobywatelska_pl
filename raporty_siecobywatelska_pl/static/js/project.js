
(function ($) {
    $('[data-toggle="sidebar"]').click(function (ev) {
       var $body = $(document.body);
       var $toggler = $(ev.target);
       var is_expanded = $($body).hasClass('sidebar-open');
       $body.toggleClass('sidebar-open', !is_expanded);
       $toggler.attr('aria-expanded', (!is_expanded).toString());
    });
} (jQuery));
