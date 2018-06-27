#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil
import platform
import re

__dir__ = os.path.dirname(os.path.abspath(__file__))


class NodePlugin(ConanFile):
    name = "tesseract.plugin"
    version = "0.1.0-dev"
    description = "Node.js addon for c plugin dynamic."
    url = "https://github.com/kedacomresearch/tesseract.plugin"
    license = "Apache-2.0"
    homepage = "https://github.com/kedacomresearch/tesseract.plugin"

    exports_sources = 'conan.cmake', 'plugin/*'
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=True", "fPIC=True")

    source_subfolder = "source_subfolder"

    def configure(self):
        self.options["tesseract"].shared = True

    def requirements(self):
        self.requires("tesseract/3.05.01@yjjnls/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")
        # self.options["tesseract.plugin"].shared = True

    def system_requirements(self):
        """ Temporary requirement until pkgconfig_installer is introduced """
        if tools.os_info.is_linux and tools.os_info.with_apt:
            installer = tools.SystemPackageTool()
            installer.install('pkg-config')

    def build(self):
        options = {
            'arch': 'x64',
            'compiler': '',
            'debug': '',
            'python': '',
        }

        if os.environ.get('PYTHON', None):
            options['python'] = '--python %s' % os.environ['PYTHON']

        if self.settings.build_type == "Debug":
            options["debug"] = "--debug"

        if platform.system() == "Windows":
            if self.settings.arch == "x86":
                options["arch"] = "ia32"

            if self.settings.compiler == "Visual Studio":
                _COMPILER = {'14': '--msvs_version=2015'}
                msvs = str(self.settings.compiler.version)
                assert (msvs in _COMPILER.keys())
                options["compiler"] = _COMPILER[msvs]

        PKG_CONFIG_PATH = ""
        for p in self.deps_cpp_info.lib_paths:
            PKG_CONFIG_PATH = "%s\\pkgconfig%s%s" % (p, os.pathsep,
                                                     PKG_CONFIG_PATH)

        vars = {'PKG_CONFIG_PATH': "%s" % PKG_CONFIG_PATH}

        cmake = CMake(self)
        with tools.environment_append(vars):
            cmake.configure(source_folder='plugin')
            cmake.build()
            # cmake.install()

    def package(self):
        ext = '.dll'
        if self.settings.os == 'Linux':
            ext = '.so'

        src = "%s" % self.settings.build_type
        self.copy(pattern='*tesseract.plugin%s' % ext, dst="bin", src=src)

        self.copy(
            pattern='tesseract.plugin.test*',
            dst="test",
            src="test/%s" % self.settings.build_type)
        self.copy(pattern='test.bmp', dst="test", src="plugin/test")

