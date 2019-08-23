
const config = {
    entry: {
        incrementApp: './src/incrementApp/incrementApp.js',
        layoutsApp: './src/layoutsApp/layoutsApp.js'
    },
    output: {
        filename: '[name].js',
        path: './build'
    },
    devtool: 'source-map',
    module: {
        rules: [
            { test: /\.(js|jsx)$/, use: 'babel-loader' }
        ]
    },
    plugins: [],
    resolve: {
        modules: [
            'src'
        ]
    }
};

module.exports = config;
