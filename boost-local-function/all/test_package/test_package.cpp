#include <boost/local_function.hpp>
#include <iostream>

int main() {
    int x = 10;
    int BOOST_LOCAL_FUNCTION(const bind x, int y) {
        return x + y;
    } BOOST_LOCAL_FUNCTION_NAME(add)

    std::cout << "Boost Local Function test package: " << add(5) << std::endl;
    return 0;
}