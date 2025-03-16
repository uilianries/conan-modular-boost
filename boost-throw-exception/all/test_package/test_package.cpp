#include <boost/throw_exception.hpp>
#include <stdexcept>
#include <iostream>

int main() {
    try {
        BOOST_THROW_EXCEPTION(std::runtime_error("Boost Throw Exception test package"));
    } catch(const std::exception& e) {
        std::cout << e.what() << std::endl;
    }
    return 0;
}