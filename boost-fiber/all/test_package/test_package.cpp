#include <boost/fiber/all.hpp>
#include <iostream>

int main() {
    boost::fibers::fiber f([]() { std::cout << "Hello from fiber\n"; });
    std::cout << "Hello from main\n";
    f.join();
    return 0;
}