#include <boost/dll/alias.hpp>
#include <boost/dll.hpp>
#include <iostream>

int my_function() {
    return 42;
}
BOOST_DLL_ALIAS(my_function, my_function)

int main() {
    std::cout << "Boost DLL test package" << std::endl;
    return 0;
}
