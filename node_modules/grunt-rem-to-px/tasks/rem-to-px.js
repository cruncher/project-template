/*
 * grunt-comment-media-queries
 * https://github.com/stephband/grunt.comment-media-queries
 */

'use strict';

module.exports = function(grunt) {

	// Please see the Grunt documentation for more information regarding task
	// creation: http://gruntjs.com/creating-tasks

	grunt.registerMultiTask('rem-to-px', 'Replace all rem values with px.', function() {

		// Merge task-specific and/or target-specific options with these defaults.
		var options = this.options({
		    	path_prefix: '/',
		    	path_images: 'images/'
		    });

		// Iterate over all specified file groups.
		this.files.forEach(function(f) {
			// Concat specified files.
			var src = f.src.filter(function(filepath) {
				// Warn on and remove invalid source files (if nonull was set).
				if (!grunt.file.exists(filepath)) {
					grunt.log.warn('Source file "' + filepath + '" not found.');
					return false;
				} else {
					return true;
				}
			}).map(function(filepath) {
				var file = grunt.file.read(filepath);

				return file

				// Replace rem values with px values
				.replace(/([+-]?\d*\.?\d+)\s*rem/g, function($0, $1, $2) {
					var rem = parseFloat($1),
					    px = Math.round(rem * 16);

					return px + 'px';
				})

				// Replace background-color rgba(r,g,b,a) with background-image: url(rgba_r_g_b_a.png);
				.replace(/background-color\s*\:\s*rgba\(\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\s*\)/g, function($0, $1, $2, $3, $4) {
					var file = options.path_images + "rgba_"+ parseInt($1) +"_"+ parseInt($2) +"_"+ parseInt($3) +"_"+ Math.round((parseFloat($4) * 100)) +".png"; 

					if (!grunt.file.exists(file)) {
						console.log('Missing image: ' + file);
					}

					return "background-image: url('" + options.path_prefix + file + "');";
				})

				// Replace opacity: x; with filter: alpha(opacity=100*x);
				.replace(/opacity\s*\:\s*(\d*\.?\d+)\s*\;/g, function($0, $1) {
					var n = parseFloat($1);
					return "filter: alpha(opacity=" + Math.round(n * 100) + "); zoom: 1;";
				});
			}).join('\n');

			// Write the destination file.
			grunt.file.write(f.dest, src);

			// Print a success message.
			grunt.log.writeln('File "' + f.dest + '" created.');
		});
	});
};
