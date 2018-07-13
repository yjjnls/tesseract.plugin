# tesseract.plugin
Plugin for Node.js to recognize stream-time by using tesseract.  
Node module node-plugin is required.

## Build
[![travis](https://www.travis-ci.org/yjjnls/tesseract.plugin/builds#)](https://www.travis-ci.org/yjjnls/tesseract.plugin)
[![Build status](https://ci.appveyor.com/api/projects/status/4pnwm14dmlgymrg8?svg=true)](https://ci.appveyor.com/project/yjjnls/tesseract-plugin)

These environment vars must be set in travis/appveyor.  

*   CONAN_USERNAME
*   CONAN_LOGIN_USERNAME
*   CONAN_PASSWORD

tesseract.plugin requires the pre-built package `tesseract.conan`, it will use the pre-built package in your own bintray defaultly.   

If you want to use the other pre-built package, set `DEPENDENT_BINTRAY_REPO` in travis/appveyor. `DEPENDENT_BINTRAY_REPO` is the bintray username, if not set, it's same as `CONAN_USERNAME`.