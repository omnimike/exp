cc_binary(
    name = "main",
    srcs = ["main.cpp"],
)

cc_test(
    name = "test-MyArray",
    srcs = ["MyArrayTest.cpp", "MyArray.h"],
    copts = ["-Iexternal/gtest/googletest/include"],
    deps = ["//external:gtest_main"],
    size = "small"
)

cc_test(
    name = "test-insertSort",
    srcs = ["insertSortTest.cpp", "insertSort.h"],
    copts = ["-Iexternal/gtest/googletest/include"],
    deps = ["//external:gtest_main"],
    size = "small"
)
