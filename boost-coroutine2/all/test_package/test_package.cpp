#include <boost/coroutine2/all.hpp>
#include <iostream>

using coro_t = boost::coroutines2::coroutine<int>;

int main() {
    coro_t::pull_type source([](coro_t::push_type& sink) {
        std::cout << "Boost Coroutine2 test package" << std::endl;
        sink(42);
    });
    return 0;
}