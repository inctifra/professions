const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack");
const Dotenv = require("dotenv-webpack");
const { BundleAnalyzerPlugin } = require("webpack-bundle-analyzer");

module.exports = {
  target: "web",
  context: path.join(__dirname, "../"),
  entry: {
    project: path.resolve(__dirname, "../static/js/project"),
    vendors: path.resolve(__dirname, "../static/js/vendors"),
    maps: path.resolve(__dirname, "../static/js/libs/maps"),
    chatbot: path.resolve(__dirname, "../static/js/libs/chatbot"),
    dashboard: path.resolve(__dirname, "../static/dashboard/js/index"),
  },
  output: {
    path: path.resolve(__dirname, "../static/webpack_bundles/"),
    publicPath: "/static/webpack_bundles/",
    filename: "js/[name]-[fullhash].js",
    chunkFilename: "js/[name]-[hash].js",
    clean: true,
  },
  plugins: [
    new BundleTracker({
      path: path.resolve(__dirname, "../static/"),
      filename: "webpack-stats.json",
    }),
    new MiniCssExtractPlugin({ filename: "css/[name].[contenthash].css" }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery",
      PureCounter: ["@srexi/purecounterjs", "default"],
      Swiper: ["swiper", "default"],
      AOS: ["aos", "default"],
      axios: "axios",
      Alpine: ["alpinejs", "default"],
      L: ["leaflet", "default"],
      Select2: ["select2", "default"],
      flatpickr: ["flatpickr", "default"],
      ApexCharts: ["apexcharts", "default"],
      SimpleBar: ["simplebar", "default"],
      "window.SimpleBar": ["simplebar", "default"],
    }),
    new Dotenv({
      path: path.resolve(__dirname, "../.env.webpack"),
      safe: true,
      allowEmptyValues: true,
      systemvars: true,
      silent: false,
      defaults: false,
      prefix: "process.env.",
    }),
    new BundleAnalyzerPlugin({
      analyzerMode: "static",
      openAnalyzer: false,
      reportFilename: "report.html",
    }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: "babel-loader",
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              url: true,
              importLoaders: 1,
            },
          },
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: ["postcss-preset-env", "autoprefixer", "pixrem"],
              },
            },
          },
          "sass-loader",
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: "asset/resource",
        generator: {
          filename: "images/[name][hash][ext][query]",
        },
      },
      {
        test: /\.(woff(2)?|eot|ttf|otf)$/,
        type: "asset/resource",
        generator: {
          filename: "fonts/[name][hash][ext]",
        },
      },
      {
        test: /\.txt$/i,
        type: "asset/resource",
        generator: {
          filename: "files/[name][hash][ext]",
        },
      },
    ],
  },
  resolve: {
    alias: {
      "@imgs": path.resolve(
        __dirname,
        "../static/dashboard/images/"
      ),
    },
    modules: ["node_modules"],
    extensions: [".js", ".jsx", ".txt"],
  },
};
