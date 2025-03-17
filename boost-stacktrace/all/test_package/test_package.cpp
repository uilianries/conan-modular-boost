#include <boost/stacktrace.hpp>
#include <iostream>

int main() {
    std::cout << "Boost Stacktrace test package " << std::endl << boost::stacktrace::stacktrace() << std::endl;
    return 0;
}