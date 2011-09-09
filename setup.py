from setuptools import setup, find_packages
 
setup(
    name='admincsvimport',
    version='0.1',
    description='Add loaddata like csv support at Django Admin Site',
    author='Terry Huang',
    author_email='terryh.tp@gmail.com',
    url='https://github.com/terryh/django-admincsvimport/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    zip_safe=False,
)
