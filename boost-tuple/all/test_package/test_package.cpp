#include <boost/tuple/tuple.hpp>
#include <iostream>

int main() {
    boost::tuple<std::string, std::string, double> t("Boost Tuple", "test package", 3.14);
    std::cout << boost::get<0>(t) << " " << boost::get<1>(t) << ": " << boost::get<2>(t) << std::endl;
    return 0;
}