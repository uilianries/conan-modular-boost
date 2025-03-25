#include <boost/beast.hpp>
#include <boost/asio.hpp>
#include <iostream>

int main() {
    boost::asio::io_context ioc;
    boost::beast::http::request<boost::beast::http::string_body> req{boost::beast::http::verb::get, "/", 11};
    std::cout << "Boost Beast test package: " << req.version() << std::endl;
    return 0;
}
