#include <boost/poly_collection/function_collection.hpp>
#include <iostream>

int main() {
    boost::function_collection<void()> functions;
    functions.insert([] { std::cout << "Boost Poly Collection test package" << std::endl; });
    for (const auto& func : functions) { func();}
    return 0;
}