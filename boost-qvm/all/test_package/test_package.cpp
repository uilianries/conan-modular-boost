#include <boost/qvm/vec.hpp>
#include <iostream>

int main() {
    boost::qvm::vec<float, 2> v = {1.0f, 2.0f};
    std::cout << "Boost QVM test package: " << v.a[0] << "," << v.a[1] << std::endl;
    return 0;
}