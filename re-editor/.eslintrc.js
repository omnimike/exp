module.exports = {
  parser: 'babel-eslint',
  env: {
    browser: true,
    commonjs: true,
    es6: true,
    node: true
  },
  extends: 'eslint:recommended',
  parserOptions: {
    ecmaFeatures: {
      experimentalObjectRestSpread: true,
      jsx: true
    },
    sourceType: 'module'
  },
  plugins: [
    'flowtype'
  ],
  settings: {
    'flowtype': {
      'onlyFilesWithFlowAnnotation': true
    }
  },
  rules: {
    'no-unused-vars': [
      'warn',
      {
        'argsIgnorePattern': '^_'
      }
    ],
    'strict': [
      'error',
      'safe'
    ],
    'indent': [
      'error',
      4
    ],
    'linebreak-style': [
      'error',
      'unix'
    ],
    'quotes': [
      'error',
      'single'
    ],
    'semi': [
      'error',
      'always'
    ],
    'no-console': ['off'],
    'flowtype/define-flow-type': 'warn',
    'flowtype/require-parameter-type': 'off',
    'flowtype/require-return-type': [
      'off',
      'always',
      {
        'annotateUndefined': 'never'
      }
    ],
    'flowtype/space-after-type-colon': [
      'warn',
      'always'
    ],
    'flowtype/space-before-type-colon': [
      'warn',
      'never'
    ],
    'flowtype/type-id-match': [
      'warn',
      '^([A-Z][a-z0-9]+)+Type$'
    ],
    'flowtype/use-flow-type': 'warn',
    'flowtype/valid-syntax': 'warn'
  }
};
