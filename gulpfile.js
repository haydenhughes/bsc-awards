var gulp = require('gulp');
var sass = require('gulp-sass');
var del = require('del')

// Compile sass into CSS & auto-inject into browsers
gulp.task('sass', function() {
    return gulp.src(['node_modules/bootstrap/scss/bootstrap.scss', 'awards/static/scss/*.scss'])
        .pipe(sass())
        .pipe(gulp.dest("awards/static/css"));
});

// Move the javascript files into our /src/js folder
gulp.task('js', function() {
    return gulp.src(['node_modules/bootstrap/dist/js/bootstrap.min.js', 'node_modules/jquery/dist/jquery.min.js', 'node_modules/popper.js/dist/umd/popper.min.js'])
        .pipe(gulp.dest("awards/static/js"));
});

gulp.task('clean', function () {
  return del(['awards/static/js/*.js', 'awards/static/css/*.css']);
});

gulp.task('default', ['clean'], function () {
  gulp.start('js');
  gulp.start('sass');
  gulp.watch(['node_modules/bootstrap/scss/bootstrap.scss', 'awards/static/scss/*.scss'], ['sass']);
});
