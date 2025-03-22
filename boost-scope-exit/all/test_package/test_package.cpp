#include <boost/scope_exit.hpp>
#include <iostream>

int main() {
    int x = 42;
    BOOST_SCOPE_EXIT(&x) {
        std::cout << "Boost Scope Exit test package: " << x << std::endl;
    } BOOST_SCOPE_EXIT_END
    return 0;
}