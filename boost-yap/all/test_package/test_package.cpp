#include <boost/yap/expression.hpp>
#include <iostream>

int main() {
    auto expr = boost::yap::make_terminal(42);
    std::cout << "Boost Yap test package: " << boost::yap::evaluate(expr) << std::endl;
    return 0;
}