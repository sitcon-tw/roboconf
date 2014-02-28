from fabric.api import local

class Compass:
	require = ['zurb-foundation']
	arguments = {
		'css_dir': 'core/static/css',
		'sass_dir': 'core/static/scss',
		'images_dir': 'core/static/img',
		'javascripts_dir': 'core/static/js',
		'output_style': 'compressed',
	}

def compass(action):
	if action == 'watch':
		local("compass watch")
	elif action == 'compile':
		commands = ["-r %s" % i for i in Compass.require]
		commands += ["--%s %s" % (k.replace('_', '-'), v) for k, v in Compass.arguments.iteritems()]
		local("compass compile " + ' '.join(commands))
	else:
		local("compass " + action)

