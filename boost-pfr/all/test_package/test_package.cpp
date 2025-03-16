#include <boost/pfr.hpp>
#include <iostream>

struct MyStruct {
    int x;
};

int main() {
    MyStruct s{42};
    std::cout << "Boost PFR test package: " << boost::pfr::get<0>(s) << std::endl;
    return 0;
}