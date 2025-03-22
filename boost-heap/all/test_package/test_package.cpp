#include <boost/heap/priority_queue.hpp>
#include <iostream>

int main() {
    boost::heap::priority_queue<int> pq;
    pq.push(10);
    std::cout << "Boost Heap test package: " << pq.top() << std::endl;
    return 0;
}