#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import platform

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
        if self.settings.os == 'Linux':
            self.run("sudo conan remote add upload_tesseract \
            https://api.bintray.com/conan/${CONAN_USERNAME}/stable --insert 0")

        # custom: requires
        self.requires("tesseract/3.05.01@yjjnls/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def build(self):
        if self.settings.os == 'Linux':
            self.run(
                "wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.1.tar.gz",
                cwd="/tmp")
            self.run("tar -zxf pkg-config-0.29.1.tar.gz", cwd="/tmp")
            self.run(
                "./configure --prefix=/usr --with-internal-glib --disable-host-tool --docdir=/usr/share/doc/pkg-config-0.29.1",
                cwd="/tmp/pkg-config-0.29.1")
            self.run("make", cwd="/tmp/pkg-config-0.29.1")
            self.run("sudo make install", cwd="/tmp/pkg-config-0.29.1")

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
            PKG_CONFIG_PATH = "%s/pkgconfig%s%s" % (p, os.pathsep,
                                                    PKG_CONFIG_PATH)

        vars = {'PKG_CONFIG_PATH': "%s" % PKG_CONFIG_PATH}

        cmake = CMake(self)
        with tools.environment_append(vars):
            cmake.configure(source_folder='plugin')
            cmake.build()
            cmake.install()

    def package(self):
        self.copy(pattern="*", dst=".", src="out")
        self.copy(pattern='test.bmp', dst="test", src="plugin/test")
