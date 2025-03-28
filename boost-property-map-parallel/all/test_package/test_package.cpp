#include <boost/property_map/parallel/local_property_map.hpp>
#include <map>
#include <iostream>

int main(int argc, char* argv[]) {
    std::map<int, std::string> storage;
    boost::associative_property_map<std::map<int, std::string>> pmap(storage);
    put(pmap, 1, "test");
    std::cout << "Boost Property Map Parallel test package" << std::endl;
    return 0;
}
