
cmake_minimum_required(VERSION 3.14)

file(GLOB SRC_FILES "*.cpp")
add_executable(hn ${SRC_FILES})
target_link_libraries(hn ${CURL_LIBRARIES} ${Folly_LIBRARIES})

