#include <boost/chrono.hpp>
#include <iostream>

int main() {
    boost::chrono::system_clock::time_point now = boost::chrono::system_clock::now();
    std::time_t time = boost::chrono::system_clock::to_time_t(now);
    std::cout << "Boost Chrono test package: " << std::ctime(&time) << std::endl;
    return 0;
}