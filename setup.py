#!/usr/bin/env python
#                   ,*++++++*,                ,*++++++*,
#                *++.        .+++          *++.        .++*
#              *+*     ,++++*   *+*      *+*   ,++++,     *+*
#             ,+,   .++++++++++* ,++,,,,*+, ,++++++++++.   *+,
#             *+.  .++++++++++++..++    *+.,++++++++++++.  .+*
#             .+*   ++++++++++++.*+,    .+*.++++++++++++   *+,
#              .++   *++++++++* ++,      .++.*++++++++*   ++,
#               ,+++*.    . .*++,          ,++*.      .*+++*
#              *+,   .,*++**.                  .**++**.   ,+*
#             .+*                                          *+,
#             *+.                   Coqui                  .+*
#             *+*              +++   TTS  +++              *+*
#             .+++*.            .          .             *+++.
#              ,+* *+++*...                       ...*+++* *+,
#               .++.    .""""+++++++****+++++++"""".     ++.
#                 ,++.                                .++,
#                   .++*                            *++.
#                       *+++,                  ,+++*
#                           .,*++++::::::++++*,.
#                                  ``````

import os
import subprocess
import sys
from distutils.version import LooseVersion

import numpy
import setuptools.command.build_py
import setuptools.command.develop
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

if LooseVersion(sys.version) < LooseVersion("3.7") or LooseVersion(sys.version) >= LooseVersion("3.11"):
    raise RuntimeError("TTS requires python >= 3.7 and < 3.11 " "but your Python version is {}".format(sys.version))


cwd = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(cwd, "TTS", "VERSION")) as fin:
    version = fin.read().strip()


class build_py(setuptools.command.build_py.build_py):  # pylint: disable=too-many-ancestors
    def run(self):
        setuptools.command.build_py.build_py.run(self)


class develop(setuptools.command.develop.develop):
    def run(self):
        setuptools.command.develop.develop.run(self)


# The documentation for this feature is in server/README.md
package_data = ["TTS/server/templates/*"]


def pip_install(package_name):
    subprocess.call([sys.executable, "-m", "pip", "install", package_name])


requirements = open(os.path.join(cwd, "requirements.txt"), "r").readlines()

with open("README.md", "r", encoding="utf-8") as readme_file:
    README = readme_file.read()

exts = [
    Extension(
        name="TTS.tts.utils.monotonic_align.core",
        sources=["TTS/tts/utils/monotonic_align/core.pyx"],
    )
]
setup(
    name="TTS",
    version=version,
    url="https://github.com/coqui-ai/TTS",
    author="Eren Gölge",
    author_email="egolge@coqui.ai",
    description="Deep learning for Text to Speech by Coqui.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MPL-2.0",
    # cython
    include_dirs=numpy.get_include(),
    ext_modules=cythonize(exts, language_level=3),
    # ext_modules=find_cython_extensions(),
    # package
    include_package_data=True,
    packages=find_packages(include=["TTS*"]),
    package_data={
        "TTS": [
            "VERSION",
        ]
    },
    project_urls={
        "Documentation": "https://github.com/coqui-ai/TTS/wiki",
        "Tracker": "https://github.com/coqui-ai/TTS/issues",
        "Repository": "https://github.com/coqui-ai/TTS",
        "Discussions": "https://github.com/coqui-ai/TTS/discussions",
    },
    cmdclass={
        "build_py": build_py,
        "develop": develop,
        # 'build_ext': build_ext
    },
    install_requires=requirements,
    python_requires=">=3.7.0, <=3.11",
    entry_points={"console_scripts": ["tts=TTS.bin.synthesize:main", "tts-server = TTS.server.server:main"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    zip_safe=False,
)
