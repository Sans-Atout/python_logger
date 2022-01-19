from setuptools import find_packages, setup

setup(
    name='python_tracer',
    packages=find_packages(include=['python_tracer']),
    version='0.1.2',
    description='My python logger packages',
    author='Sans-Atout',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
