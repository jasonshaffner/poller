from setuptools import setup

setup(name='poller',
    version='0.9',
    packages=['poller', 'poller.utils'],
    include_package_data=True,
    package_data={'poller': ['translations']},
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
