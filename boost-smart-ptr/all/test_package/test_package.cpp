#include <boost/smart_ptr.hpp>
#include <iostream>

int main() {
    boost::shared_ptr<int> ptr(new int(42));
    std::cout << "Boost Smart Pointer test package: " << ptr.use_count() << std::endl;
    return 0;
}