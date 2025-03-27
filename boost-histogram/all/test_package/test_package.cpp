#include <boost/histogram.hpp>
#include <iostream>

int main() {
    auto h = boost::histogram::make_histogram(boost::histogram::axis::regular<>(10, 0, 1));
    std::cout << "Boost Histogram test package: " << h.at(0) << std::endl;
    return 0;
}
