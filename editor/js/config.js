// hslToHex by users icl7126, Abel Rodríguez
// see: https://stackoverflow.com/questions/36721830/convert-hsl-to-rgb-and-hex
function hslToHex(h, s, l) {
    h /= 360;
    s /= 100;
    l /= 100;
    let r, g, b;
    if (s === 0) {
      r = g = b = l; // achromatic
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1 / 6) return p + (q - p) * 6 * t;
        if (t < 1 / 2) return q;
        if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
        return p;
      };
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      r = hue2rgb(p, q, h + 1 / 3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1 / 3);
    }
    const toHex = x => {
      const hex = Math.round(x * 255).toString(16);
      return hex.length === 1 ? '0' + hex : hex;
    };
    return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

var themes = {
    
    darkIce: {

        key: 'darkIce',

        colors: {
            darkGray: hslToHex(216, 41, 15),
            basicGray: hslToHex(217, 38, 33),
            paleBlue: hslToHex(210, 50, 93),
            plainWhite: hslToHex(0, 0, 100)
        },

        apply: function() {
            var colors = themes.darkIce.colors;
            config.editor.background = colors.basicGray;
            config.editor.highlight = colors.paleBlue;
            config.node.body = colors.darkGray;
            config.node.text = colors.paleBlue;
            config.node.bordercolor = colors.plainWhite;
            config.node.borderwidth = 1;
            config.edge.color = colors.paleBlue;
            config.edge.width = 3;
            config.variable.text = colors.paleBlue;
            config.variable.connector = colors.basicGray;
            config.variable.connectorUnassigned = colors.basicGray;
            config.variable.connectorAssigned = colors.plainWhite;
            config.menu.background = colors.darkGray;
            config.menu.toggle = colors.darkGray;
            config.menu.text = colors.paleBlue;
        }
    },

    vapour: {

        key: 'vapour',

        colors: {
            dark: hslToHex(265, 92, 25),
            mid: hslToHex(265, 91, 65),
            high: hslToHex(304, 92, 95),
            plainWhite: hslToHex(0, 0, 100)
        },

        apply: function() {
            var colors = themes.vapour.colors;
            config.editor.background = colors.mid;
            config.editor.highlight = colors.high;
            config.node.body = colors.dark;
            config.node.text = colors.high;
            config.node.bordercolor = colors.plainWhite;
            config.node.borderwidth = 1;
            config.edge.color = colors.high;
            config.edge.width = 3;
            config.variable.text = colors.high;
            config.variable.connector = colors.mid;
            config.variable.connectorUnassigned = colors.mid;
            config.variable.connectorAssigned = colors.plainWhite;
            config.menu.background = colors.dark;
            config.menu.toggle = colors.dark;
            config.menu.text = colors.high;
        }
    }

}

var config = {

    theme: themes.darkIce,

    editor: {
        background: hslToHex(0,0,0),
        highlight: hslToHex(0,0,0),
    },
    
    node: {
        body: hslToHex(0,0,0),
        text: hslToHex(0,0,0),
        bordercolor: hslToHex(0,0,0),
        borderwidth: 1
    },

    edge: {
        color: hslToHex(0,0,0),
        width: 1,
    },

    variable: {
        text: hslToHex(0,0,0),
        connector: hslToHex(0,0,0),
        connectorUnassigned: hslToHex(0,0,0),
        connectorAssigned: hslToHex(0,0,0),
    },

    menu: {
        background: hslToHex(0,0,0),
        toggle: hslToHex(0,0,0),
        text: hslToHex(0,0,0),
    },

    updateCSS: function() {
        var root = document.documentElement;
        root.style.setProperty('--editor-background-color', config.editor.background);
        root.style.setProperty('--menu-background-color', config.menu.background);
        root.style.setProperty('--menu-toggle-color', config.menu.toggle);
        root.style.setProperty('--menu-text-color', config.menu.text);
    },

    setup: function() {
        config.theme.apply();
        config.updateCSS();
    },

    switchTheme: function(name) {
        themes[name].apply();
        config.updateCSS();
    }

}