#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <iostream>

int main() {
    boost::geometry::model::point<double, 2, boost::geometry::cs::cartesian> point1(0.0, 0.0);
    boost::geometry::model::point<double, 2, boost::geometry::cs::cartesian> point2(1.0, 1.0);
    double distance = boost::geometry::distance(point1, point2);
    std::cout << "Boost Geometry test package: " << distance << std::endl;
    return 0;
}
