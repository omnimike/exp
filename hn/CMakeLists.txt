
cmake_minimum_required(VERSION 3.14)

project(hn)

include(CTest)

add_compile_options(
  "-std=c++17"
  "-Wall"
  "-Wpedantic"
  "-Wextra"
  "-fexceptions"
)

set(CURL_LIBRARY "-lcurl")
find_package(CURL REQUIRED)
include_directories(${CURL_INCLUDE_DIR})

# Boost
find_package(Boost 1.70 REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

# Folly
find_package(Folly REQUIRED)
find_path(Folly_ROOT_DIR
    NAMES include/folly/folly-config.h
)
find_library(Folly_LIBRARIES
    NAMES folly
    HINTS ${Folly_ROOT_DIR}/lib
)
include_directories(${Folly_INCLUDE_DIRS})

# Tests
if(BUILD_TESTING)
  add_subdirectory(vendor/googletest)
  enable_testing()
endif()

add_subdirectory(hn)
