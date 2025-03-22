#include <boost/coroutine/coroutine.hpp>
#include <iostream>

typedef boost::coroutines::coroutine<int> coro_t;

int main() {
    coro_t::pull_type source([](coro_t::push_type& sink){
        std::cout << "Boost Coroutine test package" << std::endl;
        sink(42);
    });
    return 0;
}