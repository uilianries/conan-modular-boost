#include <boost/function.hpp>
#include <iostream>

int add(int x, int y) { return x + y; }

int main() {
    boost::function<int(int,int)> func = add;
    std::cout << "Boost Function test package: " << func(40, 2) << std::endl;
    return 0;
}