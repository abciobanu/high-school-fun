cmake_minimum_required(VERSION 3.10)

# set the C++17 standard
set(CMAKE_CXX_STANDARD 17)

# set the project name
project(abc-game-of-life)

# set include directory
include_directories(include)

# set source files
file(GLOB SOURCES "src/*.cpp")

# set output path
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR})

add_executable(abc-game-of-life ${SOURCES})
