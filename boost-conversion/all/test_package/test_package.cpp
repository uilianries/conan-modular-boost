#include <boost/polymorphic_cast.hpp>
#include <boost/implicit_cast.hpp>
#include <boost/polymorphic_pointer_cast.hpp>
#include <iostream>

struct Base { virtual ~Base(){} int x = 42; };
struct Derived : Base { int y = 2; };

int main() {
    Base* b = new Derived;
    auto d = boost::polymorphic_cast<Derived*>(b);
    std::cout << "Boost Conversion test package: " << d->x << std::endl;
    delete b;

    return 0;
}