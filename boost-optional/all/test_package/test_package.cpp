#include <boost/optional.hpp>
#include <iostream>

int main() {
    boost::optional<int> opt = 42;
    std::cout << "Boost Optional test package: " << *opt << std::endl;
    return 0;
}