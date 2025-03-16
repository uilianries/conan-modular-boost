#include <boost/system/error_code.hpp>
#include <iostream>

int main() {
    boost::system::error_code ec(boost::system::errc::success, boost::system::system_category());
    std::cout << "Boost System test package: " << ec.message() << std::endl;
    return 0;
}