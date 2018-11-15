
var gulp = require('gulp');
var path = require('path');
var sass = require('gulp-sass');
var header = require('gulp-header');
var concat = require('gulp-concat');
var runSequence = require('run-sequence');
var exec = require('child_process').exec;
var package = require('./package.json');

var files = {
	css: [
		"bolt/css/normalise.css",
		"bolt/css/form.css",
		"bolt/css/block.css",
		"bolt/css/index.css",
		"bolt/css/layer.css",
		"bolt/css/card.css",
		"bolt/css/bubble.css",
		"bolt/css/button.css",
		"bolt/css/thumb.css",
		"bolt/css/text.css",
		"bolt/css/utilities.css",
		"bolt/css/dom.css",
		"bolt/css/action.css",

		"css/form.css",
		"css/block.css",
		"css/index.css",
		"css/button.css",
		"css/thumb.css",
		"css/grid.css",
		"css/text.css",
		"css/color.css",
		"css/dom.css",
		"css/space.css"
	],

	js: [
		"bolt/js/jquery-2.2.0.js",
		"bolt/js/jquery.support.inputtypes.js",
		"bolt/js/jquery.event.move.js",
		"bolt/js/jquery.event.swipe.js",
		"bolt/js/jquery.event.activate.js",
		"bolt/js/jquery.dialog.js",
		"bolt/js/jquery.transition.js",
		"bolt/js/jquery.validate.js",
		"bolt/js/bolt.js",
		"bolt/js/bolt.a.js",
		"bolt/js/bolt.dialog.js",
		"bolt/js/bolt.input.js",
		"bolt/js/bolt.input.placeholder.js",
		"bolt/js/bolt.slide.js",
		"bolt/js/bolt.tab.js",
		"bolt/js/bolt.tip.js",
		"bolt/js/bolt.toggle.js"
	]
};

var config = {
	kss: {
		title: (package.title || '') + ' Styles',

		// Directories to search for KSS comments
		source: [
			'static/bolt/css',
			'static/bolt/scss',
			'static/css'
		],

		// Directory to render styleguide
		destination: 'static/styles',

		// Location of template
		template: 'static/bolt/styles-template',

		// Relative paths to include in styleguide
		css: files.css.map(upLevel),
		js: files.js.map(upLevel)
	},

	sass: {
		source: ['static/scss/*.scss'],
		destination: 'static/css'
	},

	karma: {
		// unfortunately, karma needs the __dirname here
		//configFile: path.join(__dirname, dir.testConfig, 'karma.conf.js'),
		browsers: ['Chrome'],
		singleRun: true
	}
};

function upLevel(path) {
	return '../' + path;
}

// Lint the source files
gulp.task('lint:src', function() {
	return gulp.src([files.js])
	// eslint() attaches the lint output to the eslint property
	// of the file object so it can be used by other modules.
	.pipe($.eslint())
	// eslint.format() outputs the lint results to the console.
	// Alternatively use eslint.formatEach() (see Docs).
	.pipe($.eslint.format())
	// To have the process exit with an error code (1) on
	// lint error, return the stream and pipe to failOnError last.
	.pipe($.eslint.failOnError());
});

// Run the unit tests
gulp.task('test:spec', function(done) {
	return karma
	.start(config.karma, function(err) {
		// Stop the gulp task when an error occurs
		// in the unit tests
		if (err) {
			process.exit(1);
		}

		done();
	});
});

gulp.task('sass', function() {
  gulp.src(config.sass.source)
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest(config.sass.destination));
});

//gulp.task('build-css', function() {
//  return gulp.src(files.css)
//  // Concat files
//  .pipe(concat('bolt-' + package.version + '.css'))
//  // Add a comment to the top
//  .pipe(header('/* bolt ' + package.version + ' CSS */\n\n'))
//  // Write the file to the directory
//  .pipe(gulp.dest('./package/css/'));
//});
//
//gulp.task('build-js', function() {
//  return gulp.src(files.js)
//  // Concat files
//  .pipe(concat('bolt-' + package.version + '.js'))
//  // Add a comment to the top
//  .pipe(header('/* bolt ' + package.version + ' JS */\n\n'))
//  // Write the file to the directory
//  .pipe(gulp.dest('./package/js/'));
//});

gulp.task('kss', function(cb) {
	var command =
		'./node_modules/kss/bin/kss-node' +
		' --source '      + config.kss.source.join(' --source ') +
		' --destination ' + config.kss.destination +
		' --template '    + config.kss.template +
		' --css '         + config.kss.css.join(' --css ') +
		' --js '          + config.kss.js.join(' --js ') ;

	exec(command, function(error, stdout, stderr) {
		console.log(stdout);
		console.log(stderr);
		cb(error);
	});
});

gulp.task('default', function(done) {
	runSequence([/*'sass', 'build-css', 'build-js',*/ 'kss'], done);
});
