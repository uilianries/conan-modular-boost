#include <boost/tokenizer.hpp>
#include <iostream>

int main() {
    std::string text = "Boost Tokenizer test package";
    boost::tokenizer<> tok(text);
    for (const auto& token : tok) {
        std::cout << token << " ";
    }
    std::cout << std::endl;
    return 0;
}