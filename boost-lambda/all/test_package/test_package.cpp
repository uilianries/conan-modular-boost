#include <boost/lambda/lambda.hpp>
#include <iostream>

int main() {
    (boost::lambda::_1 > 5)(10) ? std::cout << "Boost Lambda test package" << std::endl : std::cout << "";
    return 0;
}