#include <boost/json.hpp>
#include <iostream>

int main() {
    auto parsed = boost::json::parse(R"({"answer": 42})");
    std::cout << "Boost JSON test package: " << boost::json::serialize(parsed) << std::endl;
    return 0;
}