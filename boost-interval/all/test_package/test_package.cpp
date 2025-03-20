#include <boost/numeric/interval.hpp>
#include <iostream>

int main() {
    boost::numeric::interval<double> i(1.0, 2.0);
    std::cout << "Boost Numeric Interval test package: [" << i.lower() << "," << i.upper() << "]";
    return 0;
}