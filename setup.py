from setuptools import setup

setup(
    name='pptrees',
    version='0.0.2',
    description='Parallel Prefix tree generation library',
    url='https://github.com/tdene/synth_opt_adders',
    author='tdene',
    author_email='teodord.ene@gmail.com',
    license='Apache 2.0',
    classifiers=['Development Status :: 3 - Alpha',
                'Topic :: System :: Hardware',
                'License :: OSI Approved :: Apache Software License',
                'Programming Language :: Python :: 3'],
    keywords=['hardware adders prefix'],
    package_dir={'pptrees':'src'},
    packages=['pptrees'],
    long_description=open('README.md').read(),
    install_requires=[
        "networkx",
        "pydot",
        "graphviz",
    ],
)
