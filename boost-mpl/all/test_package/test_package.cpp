#include <boost/mpl/vector.hpp>
#include <boost/mpl/at.hpp>
#include <iostream>

int main() {
    typedef boost::mpl::vector<int, double, char> types;
    std::cout << "Boost MPL test package: " << typeid(boost::mpl::at_c<types,1>::type).name() << std::endl;
    return 0;
}
