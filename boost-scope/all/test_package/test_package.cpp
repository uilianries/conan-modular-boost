#include <boost/scope/scope_exit.hpp>
#include <iostream>

int main() {
    int x = 42;
    auto cleanup = boost::scope::make_scope_exit([&] {
        std::cout << "Boost Scope test package: " << x << std::endl;
    });
    return 0;
}