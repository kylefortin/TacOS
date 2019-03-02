import setuptools
from Objects import Config

setuptools.setup(
    name='TacOS',
    version=Config.version,
    packages=setuptools.find_packages(),
    url='github.com/kylefortin/TacOS',
    license='GNU General Public License v3.0',
    author='kylefortin',
    author_email='kielfortin@gmail.com',
    description='Auxiliary lighting and accessory relay control interface.'
)
