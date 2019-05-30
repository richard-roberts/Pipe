var menu = {

    body: null,
    hidden: false,

    toggleMenu: function() {
        if (menu.hidden) {
            menu.hidden = false;
        } else {
            menu.hidden = true;
        }

        if (menu.hidden) {
            document.getElementById('menu-inner').setAttribute("style", "display:none;");
            document.getElementById('menu-toggle').setAttribute("style", "border-top-left-radius: 15px;border-bottom-left-radius: 15px;");
        } else {
            document.getElementById('menu-inner').setAttribute("style", "display:block;");
            document.getElementById('menu-toggle').setAttribute("style", "border-top-left-radius: 0px;border-bottom-left-radius: 0px;");
        }
    },

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
        document.getElementById('menu-toggle').onclick = menu.toggleMenu;
        document.getElementById('new-template-button').onclick = menu.set_new_template_menu;

    }

}