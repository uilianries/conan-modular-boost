#include <boost/url.hpp>
#include <iostream>

int main() {
    boost::urls::url u("http://conan.io");
    u.set_path("/downloads");
    std::cout << "Boost URL test package: " << u << std::endl;
    return 0;
}