#include <boost/compat/to_array.hpp>
#include <iostream>

int main() {
    int input[] = {1, 2};
    auto output = boost::compat::to_array(input);
    std::cout << "Boost Compat test package: " << output[0] << std::endl;
    return 0;
}