#include <boost/container_hash/hash.hpp>
#include <iostream>

int main() {
    boost::hash<std::string> hasher;
    std::cout << "Boost container_hash test package: " << hasher("hello") << std::endl;
    return 0;
}