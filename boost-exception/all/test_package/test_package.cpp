#include <boost/exception/all.hpp>
#include <iostream>

struct my_error : virtual std::exception, virtual boost::exception {};
void foo() { BOOST_THROW_EXCEPTION(my_error()); }

int main() {
    try {
        foo();
    } catch(const boost::exception& e) {
        std::cout << "Boost Exception test package:\n" << boost::diagnostic_information(e) << std::endl;
    }
    return 0;
}