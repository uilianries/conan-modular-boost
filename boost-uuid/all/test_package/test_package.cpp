#include <boost/uuid.hpp>
#include <iostream>

int main() {
    std::cout << "Boost UUID test package: " << boost::uuids::random_generator()() << std::endl;
    return 0;
}