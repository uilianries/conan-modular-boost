#include <boost/flyweight.hpp>
#include <iostream>

int main() {
    boost::flyweight<std::string> fw1("Boost");
    boost::flyweight<std::string> fw2("Boost");
    std::cout << "Boost Flyweight test package: " << std::boolalpha << (fw1.get() == fw2.get()) << std::endl;
    return 0;
}