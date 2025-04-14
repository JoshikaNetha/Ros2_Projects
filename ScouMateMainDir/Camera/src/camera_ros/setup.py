from setuptools import setup

package_name = 'camera_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='joshikanamani',
    maintainer_email='joshika.namani@braneenterprises.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'camera_publisher = camera_ros.camera_publisher:main',
        ],
    },
)
