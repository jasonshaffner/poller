from distutils.core import setup

setup(name='poller',
	version='0.3',
	packages=['poller'],
    scripts=['scripts/pollbase', \
            'scripts/pollmodel', \
            'scripts/pollinterfaces', \
            ],
	)

