window.setTimeout(function(){
    (function($){
        $(document)

        .on('click', '.rel-delete-link', function(e){
            e.preventDefault();
            var a = $(e.target);
            var id = a.attr('data-rel');
            var input = a.closest('div').find('input');
            var vals = input.val().split(',');
            var index = vals.indexOf(id);
            if (index > -1) {
                vals.splice(index, 1);
                input.val(vals.join(","));
                a.closest('.pill').remove();
            }

        });

    })(window.django.jQuery);
}, 500);
