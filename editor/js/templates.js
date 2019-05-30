var templates = {

    renderTemplateTreeAsInterface: function(templateList, clickCallback) {
        treeInterface = makeHtml.ul();
        editProperties.setClass(treeInterface, "template-tree");
        
        var branchRecord = {};

        function getBranchLi(path) {
            return branchRecord[path].li;
        }

        function getBranchUl(path) {
            return branchRecord[path].ul;
        }

        function createBranch(path) {
            var name = path.split(".").slice(-1)[0];
            
            var li = makeHtml.li();
            editProperties.setClass(li, "template-tree-branch");
            editInner.set(li, `${name}`);
            
            var ul =  makeHtml.ul();
            editChildren.append(li, ul);

            branchRecord[path] = {
                "ul": ul,
                "li": li
            };
        }

        function createLeaf(path) {
            var name = path.split(".").slice(-1)[0];
            var e = makeHtml.li();
            editProperties.setClickFunction(e, function() { clickCallback(path) });
            editProperties.setClass(e, "template-tree-leaf");
            var b = makeHtml.button();
            editProperties.setClass(b, "template-tree-leaf-button");
            editInner.set(b, `${name}`);
            editChildren.append(e, b);
            return e;    
        }

        function processTree(path, index) {
            var parts = path.split(".");

            if (index == (parts.length - 1)) {
            
                return createLeaf(path);        
            
            } else {
            
                var branchPath = path.split(".").slice(0, index + 1).join(".");
                
                if (!branchRecord.hasOwnProperty(branchPath)) {
                    createBranch(branchPath);
                }

                editChildren.append(
                    getBranchUl(branchPath),
                    processTree(path, index + 1)
                );

                return getBranchLi(branchPath);

            }
        }

        templateList.forEach( template => {
            editChildren.append(treeInterface, processTree(template, 0));
        });

        return treeInterface;
    }

}