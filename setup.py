import itertools

from setuptools import setup, find_packages
from xdgconfig import __version__


long_desc = ''
requirements = ['mergedeep>=1.3.4,<2']
with open('readme.md') as f:
    long_desc = f.read()


extras = {
    'jsonc': ['commentjson>=0.9.0,<1'],
    'toml': ['toml>=0.10.2,<1'],
    'yaml': ['PyYAML>=5.4.1,<6'],
    'xml': ['xmltodict>=0.12.0,<1'],
}

for k in range(2, len(extras) + 1):
    for perm in itertools.permutations(
        [x for x in extras if '+' not in x], k
    ):
        extras['+'.join(perm)] = [
            item
            for sublist in [extras[p] for p in perm]
            for item in set(sublist)
        ]

extras['all'] = [
    item
    for ex, sublist in extras.items()
    if '+' not in ex
    for item in set(sublist)
]

setup(
    name='xdgconfig',
    version=__version__,
    author='Dogeek',
    author_email='dogeek@users-noreply.github.com',
    url='https://github.com/dogeek/xdgconfig',
    description='Easy access to `~/.config`',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(),
    install_requires=requirements,
    license='MIT',
    zip_safe=True,
    platforms='any',
    python_requires='>=3.8',
    download_url='https://github.com/dogeek/xdgconfig/releases',
    extras_require=extras,
    keywords=['configuration', 'python3'],
)
