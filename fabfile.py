from fabric.api import local

class Compass:
	require = ['zurb-foundation']
	arguments = {
		'css_dir': 'core/static/css',
		'sass_dir': 'core/scss',
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

def shell():
	local('heroku run ./manage.py shell')

def log():
	local('heroku logs')

def dev():
	local('./manage.py runserver')

def deploy(branch='master'):
	local('git push heroku %s:master' % branch)
	if branch == 'master':
		local('git push origin master')
