#include <boost/redis/src.hpp>
#include <boost/asio/io_context.hpp>

int main() {
    boost::asio::io_context ioc;
    boost::redis::connection conn(ioc);
    return 0;
}