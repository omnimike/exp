#ifndef ALGOS_MYARRAY_H_
#define ALGOS_MYARRAY_H_

#include <exception>

const size_t DEFAULT_LENGTH = 16;

template <typename T>
class MyArray {
    public:
        MyArray() :
            MyArray(DEFAULT_LENGTH) {}

        MyArray(const size_t l) :
            len(l),
            arr(new T[l]) {}

        ~MyArray() {
            delete[] arr;
        }

        T at(const size_t idx) {
            if (idx >= len) {
                throw std::out_of_range("MyArray index out of bounds");
            }
            return arr[idx];
        }

        void set(const size_t idx, const T val) {
            if (idx >= len) {
                throw std::out_of_range("MyArray index out of bounds");
            }
            arr[idx] = val;
        }

        size_t length() {
            return len;
        }

    private:
        size_t len;
        T *arr;
};


#endif // ALGOS_MYARRAY_H_
