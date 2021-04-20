from setuptools import setup

setup(
    name='synth_opt_adders',
    version='0.0.1',
    author='tdene',
    author_email='teo.ene@okstate.edu',
    packages=['synth_opt_adders'],
    url='https://github.com/tdene/synth_opt_adders',
    license='LICENSE',
    description='Prefix tree adders with module boundaries drawn to optimize their implementation through synthesis and PnR tools',
    long_description=open('README.md').read(),
    install_requires=[
        "networkx",
        "pydot",
        "graphviz",
    ],
)
