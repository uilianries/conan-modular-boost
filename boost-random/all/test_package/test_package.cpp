#include <boost/random.hpp>
#include <iostream>

int main() {
    boost::random::mt19937 rng;
    std::cout << "Boost Random test package: " << rng() % 100 << std::endl;
    return 0;
}