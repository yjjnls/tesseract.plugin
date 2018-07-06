#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os
import platform


class TestPackageConan(ConanFile):
    def system_requirements(self):
        if (not os.getenv("TESSDATA_PREFIX")):
            if platform.system() == "Windows":
                tessdata_dir = "c:\\"
            else:
                tessdata_dir = "/tmp"

            if not os.path.exists("%s/nothing" % tessdata_dir):
                self.run(
                    "git clone https://github.com/yjjnls/nothing.git --depth=1",
                    cwd=tessdata_dir)

            os.environ["TESSDATA_PREFIX"] = "%s/nothing" % tessdata_dir

    def test(self):
        if platform.system() == "Windows":
            self.run("pip install cpplint")
        else:
            self.run("sudo pip install cpplint")

        # custom: source dir
        source_dir = "%s/../plugin" % os.path.dirname(__file__)

        for (root, dirs, files) in os.walk(source_dir):
            for filename in files:
                if 'nlohmann' in os.path.join(root, filename):
                    continue
                self.run(
                    "cpplint --filter=-whitespace/tab,-whitespace/braces,-build/header_guard,-readability/casting,-build/include_order,-build/include,-runtime/int --linelength=120 %s"
                    % os.path.join(root, filename))

        bin_path = ""
        if platform.system() == "Windows":
            for p in self.deps_cpp_info.bin_paths:
                bin_path = "%s%s%s" % (p, os.pathsep, bin_path)
            vars = {'PATH': "%s%s" % (bin_path, os.environ["PATH"])}
        else:
            for p in self.deps_cpp_info.lib_paths:
                bin_path = "%s%s%s" % (p, os.pathsep, bin_path)
            vars = {'LD_LIBRARY_PATH': bin_path}

        # custom: run test
        with tools.environment_append(vars):
            if platform.system() == "Windows":
                command = "tesseract.plugin.test"
            else:
                command = "./tesseract.plugin.test"
            self.run(
                command,
                cwd="%stest" %
                self.deps_cpp_info["tesseract.plugin"].build_paths[0])
