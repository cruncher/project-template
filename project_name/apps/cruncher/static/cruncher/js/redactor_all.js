var Redactor = (function ($) {
    // Redactor palette attributes will accumulate here.
    var redactor_attrs = {

        imageUpload: '/redactor-3298hjahsd2/upload/image/',
        clipboardUploadUrl: '/redactor-3298hjahsd2/paste/image/',
        fileUpload: '/redactor-3298hjahsd2/upload/file/',
        paragraphy: true,
        pastePlainText: true,
        lang: 'fr',
        minHeight: 400,
        convertDivs: false,
        plugins: ['title_style', ],
        codemirror: true,
        //linebreaks: false,
        cleanOnPaste: true
    };
    // if ("object" === typeof(document._front_edit)) {
    //     $.extend(true, redactor_attrs, document._front_edit);
    //     console.log(redactor_attrs);
    // }
    // Initialize all textareas with the ``redactor_content`` class
    // as a Redactor rich text area.
    $(document).ready(function () {
        $("textarea").each(function (i) {
            var settings = redactor_attrs[i];
            // Add a class to the field's label in the Django admin so it can
            // be styled as well.
            $(this).parent("div").find("label").addClass("redactor_label");
            $(this).redactor(redactor_attrs);
            CodeMirror.fromTextArea($(this)[0], {
                lineNumbers: true,
                mode: 'htmlmixed',
                theme: 'default'
            });
        });
    });

    return {
        register: function () {
            var attrs = arguments.length !== 0 ? arguments[0] : null;
            redactor_attrs.push(attrs);
        }
    };
})(jQuery);

