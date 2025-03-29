#include <boost/contract.hpp>
#include <iostream>

int divide(int x, int y) {
    int result;
    boost::contract::check c = boost::contract::function()
        .precondition([&] { BOOST_CONTRACT_ASSERT(y != 0); })
        .postcondition([&] { BOOST_CONTRACT_ASSERT(result * y == x); });
    return result = x / y;
}

int main() {
    std::cout << "Boost Contract test package: " << divide(10, 2) << std::endl;
    return 0;
}