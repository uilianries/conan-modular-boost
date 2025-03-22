#include <boost/signals2.hpp>
#include <iostream>

void hello() {
    std::cout << "Boost Signals2 test package" << std::endl;
}

int main() {
    boost::signals2::signal<void()> sig;
    sig.connect(&hello);
    sig();
    return 0;
}