const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require("webpack")
const Dotenv = require('dotenv-webpack');

module.exports = {
  target: 'web',
  context: path.join(__dirname, '../'),
  entry: {
    project: path.resolve(__dirname, '../professions/static/js/project'),
    vendors: path.resolve(__dirname, '../professions/static/js/vendors'),
    maps: path.resolve(__dirname, "../professions/static/js/libs/maps"),
    chatbot: path.resolve(__dirname, "../professions/static/js/libs/chatbot"),
  },
  output: {
    path: path.resolve(
      __dirname,
      '../professions/static/webpack_bundles/',
    ),
    publicPath: '/static/webpack_bundles/',
    filename: 'js/[name]-[fullhash].js',
    chunkFilename: 'js/[name]-[hash].js',
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(path.join(__dirname, '../')),
      filename: 'webpack-stats.json',
    }),
    new MiniCssExtractPlugin({ filename: 'css/[name].[contenthash].css' }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
      PureCounter: ['@srexi/purecounterjs', 'default'],
      Swiper: ['swiper', 'default'],
      AOS: ['aos', 'default'],
      axios: 'axios',
      Alpine: ['alpinejs', 'default'],
      L: ['leaflet', 'default'],
      Select2: ['select2', 'default'],
    }),
    new Dotenv({
      path: path.resolve(__dirname, "../.env.webpack"), // load this now instead of the ones in '.env'
      safe: true, // load '.env.example' to verify the '.env' variables are all set. Can also be a string to a different file.
      allowEmptyValues: true, // allow empty variables (e.g. `FOO=`) (treat it as empty string, rather than missing)
      systemvars: true, // load all the predefined 'process.env' variables which will trump anything local per dotenv specs.
      silent: false, // hide any errors
      defaults: false, // load '.env.defaults' as the default values if empty.
      prefix: 'process.env.' // reference your env variables as 'import.meta.env.ENV_VAR'.
    })
  ],
  module: {
    rules: [
      // we pass the output from babel loader to react-hot loader
      {
        test: /\.js$/,
        loader: 'babel-loader',
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              url: true,
              importLoaders: 1,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: ['postcss-preset-env', 'autoprefixer', 'pixrem'],
              },
            },
          },
          'sass-loader',
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name][hash][ext][query]'
        }
      },
      {
        test: /\.(woff(2)?|eot|ttf|otf)$/,
        type: 'asset/resource',
        generator: {
          filename: 'fonts/[name][hash][ext]',
        },
      },
    ],
  },
  resolve: {
    modules: ['node_modules'],
    extensions: ['.js', '.jsx'],
  },
};
