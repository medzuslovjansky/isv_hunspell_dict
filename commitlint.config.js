const fs = require('fs');

module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-empty': [2, 'never'],
    'scope-enum': [2, 'always', [
      ...fs.readdirSync('packages'),
      'repo',
    ]],
  }
};
