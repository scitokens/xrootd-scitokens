
cmake_minimum_required( VERSION 2.8 )
project( xrootd-scitokens )

set( CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake )
include(GNUInstallDirs)

find_package( Xrootd REQUIRED )
find_package( SciTokensCpp REQUIRED )

if(NOT XROOTD_PLUGIN_VERSION)
  find_program(XROOTD_CONFIG_EXECUTABLE xrootd-config)
  exec_program(${XROOTD_CONFIG_EXECUTABLE} ARGS "--plugin-version" OUTPUT_VARIABLE XROOTD_PLUGIN_VERSION RETURN_VALUE RETVAR)
  set(XROOTD_PLUGIN_VERSION ${XROOTD_PLUGIN_VERSION} CACHE INTERNAL "")
endif()

macro(use_cxx11)
  if (CMAKE_VERSION VERSION_LESS "3.1")
    if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
      set (CMAKE_CXX_FLAGS "-std=gnu++11 ${CMAKE_CXX_FLAGS}")
    endif ()
  else ()
    set (CMAKE_CXX_STANDARD 11)
  endif ()
endmacro(use_cxx11)
use_cxx11()

if( CMAKE_COMPILER_IS_GNUCXX )
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Werror" )
endif()
SET( CMAKE_SHARED_LINKER_FLAGS "-Wl,--no-undefined")
SET( CMAKE_MODULE_LINKER_FLAGS "-Wl,--no-undefined")

include_directories(${SCITOKENS_CPP_INCLUDE_DIR} ${XROOTD_INCLUDES} vendor/picojson vendor/inih)

add_library(XrdAccSciTokens SHARED src/XrdAccSciTokens.cc src/XrdSciTokensHelper.hh)
target_link_libraries(XrdAccSciTokens -ldl -lpthread ${SCITOKENS_CPP_LIBRARIES} ${XROOTD_UTILS_LIB} ${XROOTD_SERVER_LIB})
set_target_properties(XrdAccSciTokens PROPERTIES OUTPUT_NAME XrdAccSciTokens-${XROOTD_PLUGIN_VERSION} SUFFIX ".so" LINK_FLAGS "-Wl,--version-script=${PROJECT_SOURCE_DIR}/configs/export-lib-symbols")

SET(LIB_INSTALL_DIR "${CMAKE_INSTALL_PREFIX}/lib" CACHE PATH "Install path for libraries")

install(
  TARGETS XrdAccSciTokens
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})
