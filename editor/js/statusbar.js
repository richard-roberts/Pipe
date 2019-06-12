var logger = {
    record: [],
    
    normal: function(message) {
        console.log(message);
        logger.record.push(message);
    },
    
    warning: function(message) {
        console.warn(message);
        logger.record.push(message);
    },
    
    error: function(message) {
        console.error(message);
        logger.record.push(message);
    },
};

var statusbar = {

    left: null,
    display: null,
    right: null,
    totalSeconds: 0,

    // `getTimecodeFromSeconds` users powtac and Calvin Nunes
    // See https://stackoverflow.com/questions/6312993/javascript-seconds-to-time-string-with-format-hhmmss
    getTimecodeFromSeconds: function() {
        var hours   = Math.floor(statusbar.totalSeconds / 3600);
        var minutes = Math.floor((statusbar.totalSeconds - (hours * 3600)) / 60);
        var seconds = Math.floor(statusbar.totalSeconds - (hours * 3600) - (minutes * 60));
        if (hours   < 10) {hours   = "0"+hours;}
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        return `${hours}:${minutes}:${seconds}`;
    },

    setRightDisplayToTimecode: function() {
        editInner.set(statusbar.right, statusbar.getTimecodeFromSeconds());
    },

    updateSecondsPassedByServer: function() {
        pipe.timeSinceStart(function(seconds) {
            statusbar.totalSeconds = seconds;
            statusbar.setRightDisplayToTimecode();
        })
    },

    updateSecondsPassedByClock: function() {
        statusbar.totalSeconds += 1;
        statusbar.setRightDisplayToTimecode();
    },

    setup: function() {
        statusbar.left = document.getElementById('statusbar-left');
        statusbar.display = document.getElementById('statusbar-display');
        statusbar.right = document.getElementById('statusbar-right');

        var ip = url_base.split("//")[1].split(":")[0];
        editInner.set(statusbar.left, `${ip} >`);
        
        statusbar.updateSecondsPassedByServer();
        setInterval(statusbar.updateSecondsPassedByServer, 60000);
        setInterval(statusbar.updateSecondsPassedByClock, 1000);  
    },

    displayMessage: function(message) {
        logger.normal(message);
        editInner.set(statusbar.display, `${message}`);
    },

    displayWarning: function(message) {
        logger.warning(message);
        editInner.set(statusbar.display, `<b>Warning</b>: ${message}`);
    },

    displayError: function(message) {
        logger.error(message);
        editInner.set(statusbar.display, `<b>Error</b>: ${message}`);
    },
    

};
