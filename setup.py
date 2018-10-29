from distutils.core import setup

setup(name='poller',
	version='0.2',
	packages=['poller'],
    scripts=['scripts/pollbase', \
            'scripts/pollmodel', \
            ],
	)

