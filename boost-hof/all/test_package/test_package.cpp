#include <boost/hof.hpp>
#include <iostream>

int main() {
    const auto increment = [](int x) { return x + 1; };
    const auto square = [](int x) { return x * x; };
    std::cout << "Boost HOF compose: " << boost::hof::compose(square, increment)(2) << std::endl;
    return 0;
}
