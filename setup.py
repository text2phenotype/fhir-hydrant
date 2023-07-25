import os
from setuptools import setup, find_packages

from text2phenotype.common.test_command import TestCommand


package_dir = os.path.abspath(os.path.dirname(__file__))
requirements_files = [os.path.join(package_dir, 'requirements.txt'),
                      os.path.join(package_dir, 'fhirhydrant', 'client-requirements.txt')]
long_description = 'FHIR Fast Healthcare Interoperability Resources'


def parse_requirements(file_paths):
    req_list = []
    for file_path in file_paths:
        with open(file_path, 'r') as reqs:

            for line in reqs.readlines():
                if line.startswith('#'):
                    continue
                if line.startswith('-r '):
                    sub_req = parse_requirements(f"{line.split('-r ')[-1].replace('/n', '').strip()}")
                    req_list.extend(sub_req)
                    continue
                req_list.append(line.replace("\n", ''))
    return req_list


def select_packages():
    exclude_list = ["*.tests",
                    "*.tests.*",
                    "tests.*",
                    "tests",
                    "*.test_data.*"]

    packages = find_packages(exclude=exclude_list)
    return packages


setup(
    name='fhirhydrant',
    version='0.1.0',
    description=long_description,
    long_description=long_description,
    url='',
    author='',
    author_email='',
    license='Other/Proprietary License',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Healthcare Industry',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: FHIR (Fast Healthcare Interoperability Resources)',
    ],
    keywords=['Text2phenotype fhir-hydrant', 'python'],
    packages=select_packages(),
    install_requires=parse_requirements(requirements_files),
    include_package_data=True,
    tests_require=['pytest'],
    cmdclass={'test': TestCommand})
