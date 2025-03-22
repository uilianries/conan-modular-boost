#include <boost/filesystem.hpp>
#include <iostream>
namespace fs = boost::filesystem;

int main() {
    const boost::filesystem::path p = boost::filesystem::current_path();
    std::cout << "Boost Filesystem test package: " << p << std::endl;
    return 0;
}