var menu = {

    body: null,

    showMenu: function() {
        document.getElementById('menu-toggle').setAttribute("style", "display:none;");
        document.getElementById('menu-body').setAttribute("style", "display:block;");
    },

    hideMenu: function() {
        document.getElementById('menu-toggle').setAttribute("style", "display:block;");
        document.getElementById('menu-body').setAttribute("style", "display:none;");
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
        menu.body = document.getElementById('menu-inner');

        // Setup callbacks
        document.getElementById('hide-menu-button').onclick = menu.hideMenu;
        document.getElementById('show-menu-button').onclick = menu.showMenu;
        document.getElementById('new-template-button').onclick = menu.set_new_template_menu;

    }

}