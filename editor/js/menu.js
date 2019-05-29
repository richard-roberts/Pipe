var menu = {

    body: null,


    set_new_template_menu: function() {
        editChildren.clear(menu.body);

        pipe.list_templates(function(templateList) {
            var tree = templates.renderTemplateTreeAsInterface(
                templateList,
                function(template) {
                    console.log(`Make a new ${template} please`);
                }
            );

            editChildren.append(menu.body, tree);
        });
    },

    setup: function() {

        // Store elements 
        menu.body = document.getElementById('menu-body');

        // Setup callbacks
        document.getElementById('new-template-button').onclick = menu.set_new_template_menu;

    }

}