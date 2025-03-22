#include <boost/context/fiber.hpp>
#include <iostream>

int main() {
    boost::context::fiber f1([](boost::context::fiber&& f) {
        std::cout << "Boost Context "; return std::move(f);
    });
    f1 = std::move(f1).resume();
    std::cout << "test package" << std::endl;
    return 0;
}