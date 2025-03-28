#include <boost/python.hpp>

int main() {
    Py_Initialize();
    boost::python::exec("print('Boost Python test package')");
    return 0;
}