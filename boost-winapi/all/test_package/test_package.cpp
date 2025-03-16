#include <boost/winapi/basic_types.hpp>
#include <iostream>

int main() {
    boost::winapi::DWORD_ value = 42;
    std::cout << "Boost WinAPI test package: " << value << std::endl;
    return 0;
}