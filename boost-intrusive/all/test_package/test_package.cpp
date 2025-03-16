#include <boost/intrusive/list.hpp>
#include <iostream>

struct MyNode : boost::intrusive::list_base_hook<> {
    int data;
    MyNode(int d) : data(d) {}
};

int main() {
    boost::intrusive::list<MyNode> list;
    MyNode n1(1);
    list.push_back(n1);
    std::cout << "Boost Intrusive test package: " << list.front().data << std::endl;
    return 0;
}