#include <boost/polygon/point_data.hpp>
#include <iostream>

int main() {
    boost::polygon::point_data<int> p(5, 10);
    std::cout << "Boost Pylogon test package: (" << p.x() << ", " << p.y() << ")" << std::endl;
    return 0;
}