#include <boost/date_time/posix_time/posix_time.hpp>
#include <iostream>

int main() {
    boost::posix_time::ptime now = boost::posix_time::second_clock::local_time();
    boost::posix_time::time_duration td = boost::posix_time::hours(1) + boost::posix_time::minutes(30);
    std::cout << "Boost Date Time test package: " << now + td << std::endl;
    return 0;
}