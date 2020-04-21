var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require("gulp-uglify");
var concat = require("gulp-concat");
var cache = require('gulp-cache');
var imagemin = require('gulp-imagemin');
var bs = require('browser-sync').create();
var sass = require("gulp-sass");
// gulp-util：这个插件中有一个方法log，可以打印出当前js错误的信息
var util = require("gulp-util");
var sourcemaps = require("gulp-sourcemaps");


var path = {
    'html': './templates/**/',
    'css': './src/css/**/',
    'js': './src/js/',
    'images': './src/images/',
    'css_dist': './dist/css/',
    'js_dist': './dist/js/',
    'images_dist': './dist/images/'
};

// 处理html文件的任务
gulp.task("html",function () {
    gulp.src(path.html + '*.html')
        .pipe(bs.stream())
});

// 定义一个css的任务
gulp.task("css",function () {
    gulp.src(path.css + '*.scss')
        .pipe(sass().on("error",sass.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
});

// 定义处理js文件的任务
gulp.task("js",function () {
    gulp.src(path.js + '*.js')
        .pipe(sourcemaps.init())
        .pipe(uglify().on("error",util.log))
        .pipe(rename({"suffix":".min"}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
});

// 定义处理图片文件的任务
gulp.task('images',function () {
    gulp.src(path.images + '*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
});

// 定义监听文件修改的任务
gulp.task("watch",function () {
    gulp.watch(path.html + '*.html',['html']);
    gulp.watch(path.css + '*.scss',['css']);
    gulp.watch(path.js + '*.js',['js']);
    gulp.watch(path.images + '*.*',['images']);
});

// 初始化browser-sync的任务
gulp.task("bs",function () {
    bs.init({
        'server': {
            'baseDir': './'
        }
    });
});

// 创建一个默认的任务
gulp.task("default",['bs','watch']);
// gulp.task('default', ['watch']);