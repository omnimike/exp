#include "gtest/gtest.h"
#include "MyArray.h"
#include <exception>

TEST(MyArrayTest, HasDefaultSizeOf16) {
    MyArray<int> arr;
    int len = arr.length();
    EXPECT_EQ(len, 16);
}

TEST(MyArrayTest, CanInitializeWithCustomSize) {
    MyArray<int> arr(10);
    int len = arr.length();
    EXPECT_EQ(len, 10);
}

TEST(MyArrayTest, CanGetAndSetValues) {
    MyArray<int> arr(1);
    arr.set(0, 5);
    int valAt0 = arr.at(0);
    EXPECT_EQ(valAt0, 5);
}

TEST(MyArrayTest, AtThrowsOutOfRangeError) {
    MyArray<int> arr(1);
    ASSERT_THROW(arr.at(1), std::out_of_range);
}

TEST(MyArrayTest, AtThrowsOutOfRangeErrorForNegativeIndicies) {
    MyArray<int> arr(1);
    ASSERT_THROW(arr.at(-1), std::out_of_range);
}

TEST(MyArrayTest, SetThrowsOutOfRangeError) {
    MyArray<int> arr(1);
    ASSERT_THROW(arr.set(1, 1), std::out_of_range);
}

TEST(MyArrayTest, SetThrowsOutOfRangeErrorForNegativeIndicies) {
    MyArray<int> arr(1);
    ASSERT_THROW(arr.set(-1, 1), std::out_of_range);
}

