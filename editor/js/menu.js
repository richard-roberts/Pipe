var menu = {

    body: null,


    set_new_template_menu: function() {
        editChildren.clear(menu.body);

        pipe.list_templates(function(paths) {
            var tree = templates.renderTemplateTreeAsInterface(
                paths, editor.newNode
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