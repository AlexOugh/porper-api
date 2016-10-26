var git = require('gulp-git'),
gulp = require('gulp'),
vfs = require('vinyl-fs'),
zip = require('gulp-zip'),
exec = require('child_process').exec;

module.exports.initialize = function(cb) {
  var child = exec('npm install', function(error, stdout, stderr) {
    if (error) return cb(error);
  });
  vfs.src(['handler.py', 'config.json', 'porper/**', 'pymysql/**', 'requests/**'],{cwd:'../lambda', base:'../lambda'})
  .pipe(zip('handler.zip'))
  .pipe(gulp.dest('./particles/assets'))
  .on('end', cb);
};
