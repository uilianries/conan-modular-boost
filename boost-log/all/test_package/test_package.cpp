#include <boost/log/trivial.hpp>
#include <boost/log/utility/setup/common_attributes.hpp>

int main() {
    boost::log::add_common_attributes();
    BOOST_LOG_TRIVIAL(info) << "Boost Log test package";
    return 0;
}