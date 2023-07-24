from setuptools import setup, find_namespace_packages
setup(name='clean_folder',
      version='0.0.1',
      description='clean_folder',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder=clean_folder.main:start']}
      )     