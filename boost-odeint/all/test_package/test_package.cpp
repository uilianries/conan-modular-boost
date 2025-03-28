#include <boost/numeric/odeint.hpp>
#include <iostream>
#include <vector>

using namespace boost::numeric::odeint;

void harmonic_oscillator(const std::vector<double>& x, std::vector<double>& dxdt, double t) {
    dxdt[0] = x[0];
}

int main() {
    std::vector<double> x(1, 1.0);
    integrate(harmonic_oscillator, x, 0.0, 1.0, 0.1);
    std::cout << "Boost Numeric Odeint test package: " << x[0] << std::endl;
    return 0;
}
