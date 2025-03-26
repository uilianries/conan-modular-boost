#include <boost/contract.hpp>
#include <iostream>

int main() {
    const int foo = 42;
    BOOST_CONTRACT_PRECONDITION([] { return foo > 0; });
    std::cout << "Boost Contract test package: " << foo << std::endl;
    return 0;
}