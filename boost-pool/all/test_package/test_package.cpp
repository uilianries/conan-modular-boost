#include <boost/pool/pool.hpp>
#include <iostream>

int main() {
    boost::pool<> p(sizeof(int));
    int* ptr = static_cast<int*>(p.malloc());
    *ptr = 42;
    std::cout << "Boost Pool test package: " << *ptr << std::endl;
    p.free(ptr);
    return 0;
}