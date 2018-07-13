#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import platform
import re

__dir__ = os.path.dirname(os.path.abspath(__file__))


class NodePlugin(ConanFile):
    name = "tesseract.plugin"
    version = "0.3.0"
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

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def requirements(self):
        try:
            if self.settings.os == 'Linux':
                self.run("sudo conan remote add upload_tesseract \
                https://api.bintray.com/conan/%s/stable --insert 0 >/dev/null" %
                         os.environ.get("DEPENDENT_BINTRAY_REPO", os.environ.get("CONAN_USERNAME")))
        except Exception as e:
            print "The repo may have been added, the error above can be ignored."
        # custom: requires
        self.requires("tesseract/3.05.01@%s/stable" %
                      os.environ.get("DEPENDENT_BINTRAY_REPO", os.environ.get("CONAN_USERNAME")))

    def build_requirements(self):
        if self.settings.os == 'Linux':
            self.run(
                "if [ `expr $(pkg-config --version) \< 0.29.1` -ne 0 ]; then \
                cd /tmp \
                && wget https://pkg-config.freedesktop.org/releases/pkg-config-0.29.1.tar.gz \
                && tar -zxf pkg-config-0.29.1.tar.gz \
                && cd pkg-config-0.29.1 \
                && ./configure --prefix=/usr        \
                --with-internal-glib \
                --disable-host-tool  \
                --docdir=/usr/share/doc/pkg-config-0.29.1 \
                && make \
                && sudo make install; fi")

    def build(self):
        for p in self.deps_cpp_info.build_paths:
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
        for p in self.deps_cpp_info.build_paths:
            pc_file = self.getallfile(p)
            if pc_file:
                searchObj = re.search('/(.*)/.conan/data', pc_file)
                if searchObj:
                    self.replace_pc(pc_file, searchObj.group(1))

        if platform.system() == "Windows":
            tessdata_dir = "c:\\"
        else:
            tessdata_dir = "/tmp"

        if not os.path.exists("%s/tessdata" % tessdata_dir):
            self.run(
                "git clone https://github.com/yjjnls/tessdata.git --depth=1",
                cwd=tessdata_dir)

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
