from distutils.core import setup

setup(name='poller',
	version='0.5',
	packages=['poller'],
    scripts=['scripts/poll', \
            'scripts/pollbase', \
            'scripts/pollbulk', \
            'scripts/pollcontact', \
            'scripts/pollinterfaces', \
            'scripts/polllocation', \
            'scripts/pollmodel', \
            'scripts/pollname', \
            'scripts/walk', \
            ],
	)

