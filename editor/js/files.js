// See https://www.html5rocks.com/en/tutorials/file/dndfiles/

var files = {
    
    loadDroppedFileCotentAsString: function(e, callback) {
        e.stopPropagation();
        e.preventDefault();
        var reader = new FileReader();
        reader.onload = (function(reader)
        {
            return function()
            {
                var contents = reader.result;
                callback(contents);
            }
        })(reader);
        reader.readAsText(e.dataTransfer.files[0]);
    },
    
    showLinkIconOnDrag: function(evt) {
        evt.stopPropagation();
        evt.preventDefault();
        evt.dataTransfer.dropEffect = 'link';
    },
    
    // See https://stackoverflow.com/questions/3665115/how-to-create-a-file-in-memory-for-user-to-download-but-not-through-server
    downloadContent: function(filename, text) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    } 
}
