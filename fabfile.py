from fabric.api import cd, env, local, prefix, run, sudo

deploy_path = '/srv/http/staff.sitcon.org'

env.user = env.user.lower()
env.hosts = ['staff.sitcon.org']
env.roledefs['heroku'] = ['sitcon-staff.herokuapps.com']

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
	if 'heroku' in env.roles:
		local('heroku run ./manage.py shell')
	else:
		with cd(deploy_path), prefix('source venv/bin/activate'):
			env.output_prefix = False
			run
			run('./manage.py shell')

def log():
	if 'heroku' in env.roles:
		local('heroku logs')
	else:
		env.output_prefix = False
		run('cat /var/log/roboconf.log')

def dev():
	local('./manage.py runserver')

def deploy(branch='master'):
	if 'heroku' in env.roles:
		local('git push heroku %s:master' % branch)
	else:
		local('git push origin %s' % branch)

	if branch == 'master':
		with cd(deploy_path):
			run('git stash')
			run('git pull --rebase')
			run('git stash pop')

def restart():
	sudo('apachectl -k restart')
