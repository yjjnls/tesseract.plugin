project(tesseract.plugin)

file(GLOB_RECURSE  _SOURCES 
    ${CMAKE_CURRENT_SOURCE_DIR}/*.[ch] 
    ${CMAKE_CURRENT_SOURCE_DIR}/*.[ch]pp
    ${CMAKE_CURRENT_SOURCE_DIR}/*.cc)

include(${CMAKE_CURRENT_SOURCE_DIR}/../conan.cmake)

conan_project_group( _SOURCES ${CMAKE_CURRENT_SOURCE_DIR})
conan_find_pkgconfig( 0.29.1 )
conan_compiler_flags()
pkg_check_modules(_MODULES  REQUIRED
                   lept
                   tesseract
                 )

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${_MODULES_INCLUDE_DIRS}) 
link_directories   (${_MODULES_LIBRARY_DIRS})

add_library(tesseract.plugin  SHARED ${_SOURCES} )
target_link_libraries(tesseract.plugin ${_MODULES_LIBRARIES} )


set(instd ${CMAKE_HOME_DIRECTORY}/../out)

install(TARGETS tesseract.plugin RUNTIME DESTINATION ${instd}/bin
                                 LIBRARY DESTINATION ${instd}/lib)

add_subdirectory(test)
