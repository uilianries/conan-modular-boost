#include <boost/numeric/ublas/vector.hpp>
#include <iostream>

int main() {
    boost::numeric::ublas::vector<double> v(3);
    v[0] = 42.0;
    std::cout << "Boost Numeric Ublas test package: " << v[0] << std::endl;
    return 0;
}