const gulp = require('gulp');
const browserSync = require('browser-sync').create('dev-server');
const del = require('del');
const eslint = require('gulp-eslint');
const flow = require('gulp-flowtype');
const rollup = require('rollup');
const rollupBabelPlugin = require('rollup-plugin-babel');
const rollupPluginNode = require('rollup-plugin-node-resolve');
const rollupPluginCommonJS = require('rollup-plugin-commonjs');
const rollupPluginReplace = require('rollup-plugin-replace');
// const rollupPluginUglify = require('rollup-plugin-uglify');

const SRC_DIR = './client';
const PAGES_DIR = SRC_DIR + '/pages';
const ALL_JS_FILES = SRC_DIR + '/**/*.js';
const ENTRY_SCRIPT = SRC_DIR + '/pages/index.js';
const BUILD_DIR = './build';
const BUNDLE_FILE = BUILD_DIR + '/bundle.js';

let bundleCache = null;

gulp.task('default', ['build']);

gulp.task('serve', ['build'], () => {
  browserSync.init({
    server: {
      baseDir: BUILD_DIR
    }
  });

  gulp.watch(SRC_DIR + '/**/*', ['serve:reload']);
});

gulp.task('serve:reload', ['build'], () => {
  browserSync.reload();
});

gulp.task('build', ['build:html', 'build:js']);

gulp.task('clean', () => {
  return del(BUILD_DIR);
});

gulp.task('build:html', ['clean:html'], () => {
  return gulp.src(PAGES_DIR + '/*.html')
    .pipe(gulp.dest(BUILD_DIR));
});

gulp.task('clean:html', () => {
  return del(BUILD_DIR + '/**/*.html');
});

gulp.task('build:js', ['clean:js'], () => {
  return rollup.rollup({
    entry: ENTRY_SCRIPT,
    cache: bundleCache,
    plugins: [
      rollupBabelPlugin({
        exclude: 'node_modules/**',
      }),
      rollupPluginReplace({'process.env.NODE_ENV': JSON.stringify('development')}),
      rollupPluginNode({
        jsnext: true,
        main: true,
        browser: true
      }),
      rollupPluginCommonJS({
        include: 'node_modules/**',
        exclude: ['node_modules/symbol-observable/**']
      })
    ]
  }).then((bundle) => {
    bundleCache = bundle;
    return bundle.write({
      format: 'es',
      dest: BUNDLE_FILE,
      sourceMap: true
    });
  });
});

gulp.task('flow:watch', () => {
  gulp.watch(SRC_DIR + '/**/*', ['flow']);
});

gulp.task('flow', () => {
  gulp.src(ALL_JS_FILES)
    .pipe(flow({
      weak: false,
      killFlow: false
    }));
});

gulp.task('lint', ['lint:js']);

gulp.task('lint:js', () => {
  gulp.src(ALL_JS_FILES)
    .pipe(eslint())
    .pipe(eslint.format())
    .pipe(eslint.failAfterError());
});

gulp.task('clean:js', () => {
  return del([BUILD_DIR + '/**/*.js', BUILD_DIR + '/**/*.js.map']);
});
