#include <boost/parameter.hpp>
#include <iostream>

BOOST_PARAMETER_NAME(value)

template<class ArgumentPack>
void show(const ArgumentPack& args) {
    std::cout << "Boost Parameter test package: " << args[_value] << std::endl;
}

int main() {
    show((_value = 42));
    return 0;
}