from setuptools import setup

LONG_DESCRIPTION = """
Find words four letters or more from a group of seven letters

"""

setup(
    name='wordgame',
    version='0.0.1',
    description='A word game',
    long_description=LONG_DESCRIPTION,
    license='MIT',
    packages=['wordgame'],
    install_requires=[
          'pandas'
      ]
    author='A true artist',
    author_email='stuart.harty@email.com',
    keywords=['games', 'vocabulary'],
    url='https://github.com/sbha/wordgame.py'
)


