#include <boost/units/systems/si.hpp>
#include <iostream>

int main() {
    using namespace boost::units::si;
    boost::units::quantity<boost::units::si::length> l = 2.0 * boost::units::si::meters;
    std::cout << "Boost Units test package: " << l.value() << std::endl;
    return 0;
}
