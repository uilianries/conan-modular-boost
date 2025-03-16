#include <boost/io/ios_state.hpp>
#include <iostream>

int main() {
    boost::io::ios_flags_saver ifs(std::cout);
    std::cout << "Boost IO test package: " << std::hex << 16 << std::endl;
    return 0;
}