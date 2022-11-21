//
// Nezrena Mail - Config
// Illia Yavdoshchuk (c) 2022
//

const fs = require("fs");
const homepath = require("./homepath")
var config = { load };

function load() {
    Object.assign(config, JSON.parse(fs.readFileSync(homepath("config.json")).toString()))
    config.load = load;
}

module.exports = config;