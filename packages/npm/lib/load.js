var read = require('fs').readFile;
var join = require('path').join;

function exportLoader(lang) {
  return function loadDictionary(callback) {
    var pos = -1;
    var exception = null;
    var result = {};

    one('aff');
    one('dic');

    function one(name) {
      read(join(__dirname, '..', 'dict', lang + '.' + name), function (err, doc) {
        pos++;
        exception = exception || err;
        result[name] = doc;

        if (pos) {
          callback(exception, exception ? null : result);
          exception = null;
          result = null;
        }
      });
    }
  };
}

module.exports = exportLoader;
