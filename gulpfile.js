
////////////////////////////////
		//Setup//
////////////////////////////////

var path = require('path');
var fs = require('fs');
var pjson = require('./package.json');

// Plugins
var gulp = require('gulp'),
      sass = require('gulp-sass'),
      autoprefixer = require('gulp-autoprefixer'),
      cssnano = require('gulp-cssnano'),
      concat = require('gulp-concat'),
      rename = require('gulp-rename'),
      plumber = require('gulp-plumber'),
      pixrem = require('gulp-pixrem'),
      uglify = require('gulp-uglify'),
      imagemin = require('gulp-imagemin'),
      runSequence = require('run-sequence');

var browserSync = require('browser-sync').create(),
  reload = browserSync.reload;
var isDocker = fs.existsSync("/.dockerenv")


// Relative paths function
var pathsConfig = function (appName) {
  this.app = "./" + (appName || pjson.name);

  return {
    app: this.app,
    templates: this.app + '/templates',
    css: this.app + '/static/css',
    sass: this.app + '/assets/sass',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/images',
    js: {
      src: [
          '/node_modules/d3/build/d3.js',
          '/node_modules/nvd3/build/nv.d3.js',
          this.app + '/assets/js/**/*.js'
      ],
      dest: this.app + '/static/js/project.js'
    }
  }
};

var paths = pathsConfig();

////////////////////////////////
		//Tasks//
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/*.scss')
    .pipe(sass({
        includePaths: ['./node_modules']
    }).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 versions']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(gulp.dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.css));
});

// Javascript minification
gulp.task('scripts', function() {
  return gulp.src(paths.js.src)
    .pipe(plumber()) // Checks for errors
    .pipe(concat(path.basename(paths.js.dest)))
    .pipe(gulp.dest(path.dirname(paths.js.dest)))
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(path.dirname(paths.js.dest)));
});

// Image compression
gulp.task('imgCompression', function(){
  return gulp.src(paths.images + '/*')
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(gulp.dest(paths.images))
});


// Browser sync server for live reload
gulp.task('browserSync', function() {
    browserSync.init([
      paths.css + "/*.css",
      paths.js + "*.js",
      paths.templates + '*.html'
    ],{
      proxy:  isDocker ? "web:8000" : "localhost:8000",
      open: !isDocker
    });
});

// Watch
gulp.task('watch', function() {
  gulp.watch(paths.sass + '/**/*.scss', ['styles']);
  gulp.watch(paths.js.src, ['scripts']).on("change", reload);
  gulp.watch(paths.images + '/*', ['imgCompression']);
  gulp.watch(paths.templates + '/**/*.html').on("change", reload);
});

// Default task
gulp.task('default', function() {
    runSequence(
      ['styles', 'scripts', 'imgCompression'],
      ['browserSync', 'watch']
    );
});
