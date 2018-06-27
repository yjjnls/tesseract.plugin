#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os
import platform


class TestPackageConan(ConanFile):
    def system_requirements(self):
        if (not os.getenv("TESSDATA_PREFIX")):
            self.run(
                "git clone https://github.com/yjjnls/nothing.git --depth=1",
                cwd=self.deps_cpp_info["tesseract.plugin"].build_paths[0])
            os.environ["TESSDATA_PREFIX"] = "%snothing" % self.deps_cpp_info[
                "tesseract.plugin"].build_paths[0]

    def test(self):
        if platform.system() == "Windows":
            self.run("pip install cpplint")
        else:
            self.run("sudo pip install cpplint")

        source_dir = "%s/../plugin" % os.path.dirname(__file__)
        for (root, dirs, files) in os.walk(source_dir):
            for filename in files:
                # print os.path.join(root,filename)
                if 'nlohmann' in os.path.join(root, filename):
                    continue
                self.run(
                    "cpplint --filter=-whitespace/tab,-whitespace/braces,-build/header_guard,-readability/casting,-build/include_order,-build/include,-runtime/int --linelength=120 %s"
                    % os.path.join(root, filename))

        bin_path = ""
        for p in self.deps_cpp_info.bin_paths:
            bin_path = "%s%s%s" % (p, os.pathsep, bin_path)
        if platform.system() == "Windows":
            vars = {'PATH': "%s%s" % (bin_path, os.environ["PATH"])}
        else:
            vars = {'LD_LIBRARY_PATH': bin_path}

        with tools.environment_append(vars):
            self.run(
                "tesseract.plugin.test",
                cwd="%stest" %
                self.deps_cpp_info["tesseract.plugin"].build_paths[0])
