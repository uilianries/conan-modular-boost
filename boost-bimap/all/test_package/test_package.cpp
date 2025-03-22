#include <boost/bimap.hpp>
#include <iostream>

int main() {
    boost::bimap<std::string, int> bm;
    bm.insert({"Boost Bimap test package", 1});
    std::cout << bm.right.at(1) << std::endl;
    return 0;
}