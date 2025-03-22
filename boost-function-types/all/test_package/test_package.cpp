#include <boost/function_types/result_type.hpp>
#include <boost/function_types/parameter_types.hpp>
#include <iostream>

typedef int (*func_type)(double, char);

int main() {
    std::cout << "Boost Function Types test package: " << typeid(boost::function_types::result_type<func_type>::type).name() << std::endl;
    return 0;
}