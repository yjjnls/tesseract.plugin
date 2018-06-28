project(tesseract.plugin.test)

file(GLOB_RECURSE  _SOURCES 
     ${CMAKE_CURRENT_SOURCE_DIR}/*.[ch] 
     ${CMAKE_CURRENT_SOURCE_DIR}/*.[ch]pp
     ${CMAKE_CURRENT_SOURCE_DIR}/*.cc)

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${_MODULES_INCLUDE_DIRS}) 
link_directories   (${_MODULES_LIBRARY_DIRS})

add_executable(tesseract.plugin.test ${_SOURCES} )
target_link_libraries(tesseract.plugin.test ${_MODULES_LIBRARIES} )


set(instd ${CMAKE_HOME_DIRECTORY}/../out)

install(TARGETS tesseract.plugin.test RUNTIME DESTINATION ${instd}/test)
