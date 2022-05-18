from setuptools import setup, find_namespace_packages

setup(
    name="pptrees",
    version="0.0.2",
    description="Parallel Prefix tree generation library",
    url="https://github.com/tdene/synth_opt_adders",
    author="tdene",
    author_email="teodord.ene@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    keywords=["hardware adders prefix"],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    package_data={"pptrees": ["mappings/*.v"]},
    long_description=open("README.md").read(),
    python_requires=">=3.7.*",
    install_requires=["networkx", "pydot", "graphviz", "Pillow"],
)
