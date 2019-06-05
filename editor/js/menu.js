var menu = {

    body: null,
    open: true,

    showMenu: function() {
        menu.open = true;
        document.getElementById('menu-toggle').setAttribute("style", "display:none;");
        document.getElementById('menu-body').setAttribute("style", "display:block;");
    },

    hideMenu: function() {
        menu.open = false;
        document.getElementById('menu-toggle').setAttribute("style", "display:block;");
        document.getElementById('menu-body').setAttribute("style", "display:none;");
    },

    newNodeMenu: function() {
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
        document.getElementById('menu-toggle').onclick = menu.showMenu;
        document.getElementById('new-node-button').onclick = menu.newNodeMenu;
        document.getElementById('export-graph-button').onclick = editor.exportToFile;
    }

}