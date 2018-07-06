#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
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
        if self.settings.os == 'Linux':
            if not os.getenv('PKG_CONFIG_EXECUTABLE'):
                self.run(
                    "wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.1.tar.gz",
                    cwd="/tmp")
                self.run("tar -zxf pkg-config-0.29.1.tar.gz", cwd="/tmp")
                self.run(
                    "./configure --prefix=/usr --with-internal-glib --disable-host-tool --docdir=/usr/share/doc/pkg-config-0.29.1",
                    cwd="/tmp/pkg-config-0.29.1")
                self.run("make", cwd="/tmp/pkg-config-0.29.1")
                self.run("sudo make install", cwd="/tmp/pkg-config-0.29.1")

        try:
            if self.settings.os == 'Linux':
                self.run("sudo conan remote add upload_tesseract \
                https://api.bintray.com/conan/${CONAN_USERNAME}/stable --insert 0"
                         )
        except Exception as e:
            print "The repo may have been added, the error above can be ignored."
        # custom: requires
        self.requires("tesseract/3.05.01@yjjnls/stable")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def build(self):
        for p in self.deps_cpp_info.lib_paths:
            pc_file = self.getallfile(p)
            if pc_file:
                searchObj = re.search('/(.*)/.conan/data', pc_file)
                if searchObj:
                    self.replace_pc(pc_file, searchObj.group(1))
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

    def package_info(self):
        for p in self.deps_cpp_info.lib_paths:
            pc_file = self.getallfile(p)
            if pc_file:
                searchObj = re.search('/(.*)/.conan/data', pc_file)
                if searchObj:
                    self.replace_pc(pc_file, searchObj.group(1))

    def getallfile(self, path):
        allfilelist = os.listdir(path)
        for file in allfilelist:
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                res = self.getallfile(filepath)
                if res:
                    return res
            if ".pc" in filepath:
                return filepath

    def replace_pc(self, target_file, target_dir):
        file_object = open(target_file, 'r+')
        try:
            all_lines = file_object.readlines()
            file_object.seek(0)
            file_object.truncate()
            for line in all_lines:
                if '.conan/data' in line:
                    searchObj = re.search('/(.*)/.conan/data', line)
                    if searchObj:
                        line = line.replace("%s" % searchObj.group(1),
                                            target_dir)
                file_object.write(line)
        finally:
            file_object.close()
