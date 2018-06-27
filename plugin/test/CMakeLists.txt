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


set(instd ${CMAKE_HOME_DIRECTORY}/bin)
if( MSVC )
	set(instd ${instd}/win )
else()
	set(instd ${instd}/linux )
endif()

if(${CMAKE_SYSTEM_PROCESSOR} STREQUAL AMD64 OR ${CMAKE_SYSTEM_PROCESSOR} STREQUAL x86_64)
    set(instd "${instd}/x64")
else()
	set(instd "${instd}/x86")
endif()
message ("${instd}")

install(TARGETS tesseract.plugin.test RUNTIME DESTINATION ${instd}
                                 LIBRARY DESTINATION ${instd})
