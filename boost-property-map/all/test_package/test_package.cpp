#include <boost/property_map/property_map.hpp>
#include <map>
#include <iostream>

int main() {
    std::map<int, std::string> data;
    data[1] = "Boost Property Map ";
    data[2] = "test package";

    boost::associative_property_map<std::map<int, std::string>> prop_map(data);

    std::cout << get(prop_map, 1) << get(prop_map, 2) << std::endl;
    return 0;
}