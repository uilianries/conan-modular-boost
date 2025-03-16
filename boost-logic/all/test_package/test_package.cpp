#include <boost/logic/tribool.hpp>
#include <iostream>

int main() {
    boost::logic::tribool t(boost::logic::indeterminate);
    std::cout << "Boost Logic test package: " << boost::logic::indeterminate(t) << std::endl;
    return 0;
}