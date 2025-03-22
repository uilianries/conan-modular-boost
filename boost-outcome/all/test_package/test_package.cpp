#include <boost/outcome.hpp>
#include <iostream>

int main() {
    boost::outcome_v2::result<int> r{42};
    std::cout << "Boost Outcome test package: " << r.value() << std::endl;
    return 0;
}