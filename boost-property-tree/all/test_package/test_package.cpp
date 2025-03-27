#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <iostream>

int main() {
    boost::property_tree::ptree pt;
    pt.put("message", "Boost Property Tree test package");
    std::cout << pt.get<std::string>("message") << std::endl;
    return 0;
}
