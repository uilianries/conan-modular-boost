#include <boost/charconv.hpp>
#include <iostream>

int main() {
    char buffer[] = "12345"; int value;
    boost::charconv::from_chars(buffer, buffer + 5, value);
    std::cout << "Boost Chanconv test package: " << value << std::endl;
    return 0;
}