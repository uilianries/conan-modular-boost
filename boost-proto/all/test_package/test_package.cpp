#include <boost/proto/proto.hpp>
#include <iostream>

int main() {
    boost::proto::terminal<int>::type _1 = {1}, _2 = {2};
    auto expr = _1 + _2;
    std::cout << "Boost Proto test package: " << boost::proto::value(boost::proto::left(expr)) << std::endl;
    return 0;
}