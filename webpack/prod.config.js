const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');
const TerserPlugin = require('terser-webpack-plugin');

const staticUrl = '/static/';

module.exports = merge(commonConfig, {
  mode: 'production',
  devtool: 'source-map',
  bail: true,
  output: {
    publicPath: `${staticUrl}webpack_bundles/`,
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        extractComments: false,
        terserOptions: {
          compress: true,
          mangle: true,
          output: {
            comments: false,
          },
        },
      }),
    ],
  },
});
