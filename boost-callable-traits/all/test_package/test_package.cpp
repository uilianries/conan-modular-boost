#include <boost/callable_traits.hpp>
#include <iostream>

int main() {
    using func_t = int(float, double);
    using args = boost::callable_traits::args_t<func_t>;
    using ret = boost::callable_traits::return_type_t<func_t>;
    std::cout << "Return type is int: " << std::is_same_v<ret, int> << std::endl;
    return 0;
}
