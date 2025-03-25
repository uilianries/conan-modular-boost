#include <boost/thread.hpp>
#include <iostream>

void print() {
    std::cout << "Boost Thread test package" << std::endl;
}

int main() {
    boost::thread t(print);
    t.join();
    return 0;
}
