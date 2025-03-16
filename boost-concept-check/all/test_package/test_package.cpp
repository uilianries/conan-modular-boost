#include <boost/concept_check.hpp>
#include <vector>
#include <iostream>


int main() {
    BOOST_CONCEPT_ASSERT((boost::RandomAccessContainer<std::vector<int>>));
    std::cout << "Boost Concept Check test package" << std::endl;
    return 0;
}