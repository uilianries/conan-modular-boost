#include <boost/align/aligned_alloc.hpp>
#include <boost/align/is_aligned.hpp>
#include <iostream>

int main() {
    void* ptr = boost::alignment::aligned_alloc(16, 32);
    std::cout << "Boost Align test package: " << boost::alignment::is_aligned(16, ptr) << std::endl;
    boost::alignment::aligned_free(ptr);
    return 0;
}