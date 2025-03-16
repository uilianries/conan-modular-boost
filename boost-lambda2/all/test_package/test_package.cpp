#include <boost/lambda2.hpp>
#include <iostream>

int main() {
    using namespace boost::lambda2;
    const auto result = (_1 + _2 * _3)( 1, 2, 3) == 1 + 2 * 3 ? 0: 1;
    std::cout << "Boost Lambda2 result: " << result << std::endl;
    return 0;
}
