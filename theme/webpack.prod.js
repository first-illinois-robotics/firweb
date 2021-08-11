const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CompressionPlugin = require("compression-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const path = require("path");
const HtmlWebpackPluginDjango = require("html-webpack-plugin-django");

module.exports = merge(common, {
    mode: 'production',
    devtool: "source-map",
    bail: true,
    output: {
        filename: "js/[name].[chunkhash:8].js",
        chunkFilename: "js/[name].[chunkhash:8].chunk.js",
        publicPath: "static/"
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "css/[name].[contenthash].css",
        }),
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, './asset-tags.ejs'),
            filename: path.resolve(__dirname, '../firweb/templates/generated/asset-tags.html'),
            inject:false,
        }),
        new HtmlWebpackPluginDjango({ bundlePath: "" }),
        new CompressionPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.ts$/,
                exclude: /node_modules/,
                use: "ts-loader",
            },
            {
                test: /\.s?css/i,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "postcss-loader",
                    "sass-loader",
                ],
            },
        ],
    },
});
