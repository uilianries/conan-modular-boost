#include <boost/regex.hpp>
#include <boost/log/trivial.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>
#include <iostream>

int main() {
    boost::log::add_common_attributes();
    BOOST_LOG_TRIVIAL(info) << "Boost Log test package";
    boost::regex pat("([0-9]+)");
    std::cout << "Boost Regex test package: " << boost::regex_match("123", pat);
    return 0;
}