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

    newTemplateMenu: function() {
        editChildren.clear(menu.body);

        var items = [];
        ["py", "c", "rb", "sh", "bat"].forEach( ext => {
            var item = `<option value="${ext}">${ext}</option>`;
            items.push(item);
        });

        var inner = `

            <div class="menu-inner-container">

                <div class="menu-small-section"></div>
            
                <div class="menu-small-section">
                    <div class="menu-small-section-inner">
                        <div>Path</div>
                    </div>
                    <div class="menu-large-section-inner">
                        <input id="new-template-menu-path" type="text"></input>
                    </div>
                </div>

                <div class="menu-small-section">
                    <div class="menu-small-section-inner">
                        <div>Type</div>
                    </div>
                    <div class="menu-large-section-inner">
                        <select id="new-template-menu-ext"> ${items}</select>
                    </div>
                </div>

                <div class="menu-small-section">
                    <div class="menu-small-section-inner">
                        <div>Arguments</div>
                    </div>
                    <div class="menu-large-section-inner">
                        <input id="new-template-menu-args" type="text"></input>
                    </div>
                </div>

                <div class="menu-small-section">
                    <div class="menu-small-section-inner">
                        <div>Outputs</div>
                    </div>
                    <div class="menu-large-section-inner">
                        <input id="new-template-menu-outs" type="text"></input>
                    </div>
                </div>

                <div class="menu-small-section"></div>

                <div class="menu-full-section-inner" id="code-container">
                    <div id="code-editor"></div>
                </div>

                <div class="menu-small-section"></div>

                <div class="menu-small-section">
                    <div class="menu-small-section-inner">
                        <button id="new-template-menu-submit">Submit</button>
                    </div>
                    <div class="menu-large-section-inner">
                    </div>
                </div>

            </div>
        `

        editInner.set(menu.body, inner);

        var codeEditor = ace.edit("code-editor");
        codeEditor.setTheme("ace/theme/monokai");
        codeEditor.session.setMode("ace/mode/python");

        document.getElementById('new-template-menu-submit').onclick = function(e) {
            var path = document.getElementById("new-template-menu-path").value;
            var ext = document.getElementById("new-template-menu-ext").value;
            var argStr = document.getElementById("new-template-menu-args").value;
            var outStr = document.getElementById("new-template-menu-outs").value;
            var code = codeEditor.getValue();

            var args = "[";
            if (argStr == "") {
                args = "[]";
            } else {
                args = "[";
                argParts = argStr.split(",");
                argParts.forEach( part => {
                    args += `"${part}",`;
                });
                args = args.substring(0, args.length - 1) + "]";
            }

            var outs;
            if (outStr == "") {
                outs = "[]";
            } else {
                outs = "[";
                outParts = outStr.split(",");
                outParts.forEach( part => {
                    outs += `"${part}",`;
                });
                outs = outs.substring(0, outs.length - 1) + "]";
            }
            
            editor.newTemplate(path, args, outs, ext, code);
            editChildren.clear(menu.body);
            menu.hideMenu();
        }
        
        // Drop event
        document.getElementById('code-editor').ondragover = files.showLinkIconOnDrag;
        document.getElementById('code-editor').ondrop = function(e) {
            files.loadDroppedFileCotentAsString(e, function(str) {
                codeEditor.setValue(str);
            });
        }

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

    uploadMenu: function() {
        editChildren.clear(menu.body);

        var inner = `

            <div class="menu-inner-container">

                <div class="menu-small-section"></div>

                <form id="upload-menu-form" method="POST" enctype="multipart/form-data">
                    <div class="menu-small-section"></div>
                            <div class="menu-small-section-inner">
                                <div>Key</div>
                            </div>
                            <div class="menu-large-section-inner">
                                <input name="path" type="text" id="upload-menu-form-path"></input>
                            </div>

                            <div class="menu-small-section-inner">
                                <input name="file" type="file">
                            </div>
                            <div class="menu-large-section-inner"></div>

                            <div class="menu-small-section-inner">
                                <input type="submit" value="Upload" />
                            </div>
                            <div class="menu-large-section-inner"></div>
                    </div>

                </form>

            </div>
        `

        editInner.set(menu.body, inner);

        var path = document.getElementById("upload-menu-form-path");
        path.value = "Files.";

        var form = document.getElementById("upload-menu-form");
        form.onsubmit = function() {
            pipe.upload(form, function(response) {
                editChildren.clear(menu.body);
                menu.hideMenu();
            });
            return false;
        }
    },

    settingsMenu: function() {

        var items = [];
        ["darkIce", "vapour"].forEach( theme => {
            var item = `<option value="${theme}">${theme}</option>`;
            items.push(item);
        });

        var inner = `

            <div class="menu-inner-container">

                <div class="menu-small-section"></div>

                <div class="menu-small-section">
                    <div class="menu-small-section-inner">
                        <div>Theme</div>
                    </div>
                    <div class="menu-large-section-inner">
                        <select id="settings-menu-theme"> ${items}</select>
                    </div>
                </div>

                <div class="menu-small-section">
                    <div class="menu-small-section-inner">
                        <div>Zoom Speed</div>
                    </div>
                    <div class="menu-large-section-inner">
                        <input id="settings-menu-scroll" type="text"></input>
                    </div>
                </div>

            </div>
        `

        editInner.set(menu.body, inner);

        var theme = document.getElementById('settings-menu-theme');
        theme.value = config.theme.key;
        
        theme.onchange = function(e) {
            config.switchTheme(theme.value);
            editor.refresh();
        }

        var scrollSpeed = document.getElementById('settings-menu-scroll');
        scrollSpeed.value = config.scrollSpeed;
        scrollSpeed.onchange = function(e) {
            config.scrollSpeed = parseFloat(scrollSpeed.value);
        }

    },

    setup: function() {

        // Store elements 
        menu.body = document.getElementById('menu-inner');

        // Setup callbacks
        document.getElementById('menu-toggle').onclick = menu.showMenu;
        document.getElementById('new-template-button').onclick = menu.newTemplateMenu;
        document.getElementById('new-node-button').onclick = menu.newNodeMenu;
        document.getElementById('upload-file-button').onclick = menu.uploadMenu;
        document.getElementById('export-graph-button').onclick = editor.exportToFile;
        document.getElementById('settings-button').onclick = menu.settingsMenu;
    }

}