#include <boost/unordered_map.hpp>
#include <iostream>

int main() {
    boost::unordered_map<std::string, int> map{{"one", 1}, {"two", 2}, {"three", 3}};
    std::cout << "Boost Unordered test package: " << map["two"] << std::endl;
    return 0;
}