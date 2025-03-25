#include <boost/icl/interval_set.hpp>
#include <iostream>

int main() {
    boost::icl::interval_set<int> set;
    set.insert(boost::icl::interval<int>::right_open(1, 5));
    std::cout << "Boost ICL test package: " << set << std::endl;
    return 0;
}
