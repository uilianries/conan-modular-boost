#include <boost/locale.hpp>
#include <iostream>

int main() {
    boost::locale::generator gen;
    std::locale::global(gen("en_US.UTF-8"));
    std::cout << boost::locale::translate("Boost Locale test package") << std::endl;
    return 0;
}