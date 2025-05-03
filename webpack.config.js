const path = require('path');

module.exports = {
  mode: 'development',
  entry: './javascript/mobile_verification.js',
  output: {
    filename: 'mobile_verification.js',
    path: path.resolve(__dirname, 'static'),
  },
}
