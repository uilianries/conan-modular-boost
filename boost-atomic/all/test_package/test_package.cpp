#include <boost/atomic.hpp>
#include <iostream>

int main() {
    boost::atomic<int> atomic_counter(0);
    std::cout << "Boost Atomic test package: " << atomic_counter.fetch_add(1) << std::endl;
    return 0;
}