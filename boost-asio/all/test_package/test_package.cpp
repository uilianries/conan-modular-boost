#include <boost/asio.hpp>
#include <iostream>

int main() {
    boost::asio::io_context io;
    boost::asio::steady_timer timer(io, boost::asio::chrono::seconds(1));
    std::cout << "Boost ASIO test package" << std::endl;
    return 0;
}
