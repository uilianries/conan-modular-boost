#include <boost/foreach.hpp>
#include <string>
#include <vector>
#include <iostream>

int main() {
    std::vector<std::string> words = {"Boost", "Foreach", "test", "package"};
    BOOST_FOREACH(const std::string& word, words) {
        std::cout << word << " ";
    }
    std::cout << std::endl;
    return 0;
}