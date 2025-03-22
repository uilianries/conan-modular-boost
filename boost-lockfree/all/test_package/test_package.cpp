#include <boost/lockfree/queue.hpp>
#include <iostream>

int main() {
    boost::lockfree::queue<int> q(10);
    q.push(42);
    int value;
    if (q.pop(value)) {
        std::cout << "Boost Lockfree test package: " << value << std::endl;
    }
    return 0;
}