#include <boost/gil.hpp>
#include <boost/gil/extension/io/jpeg.hpp>
#include <boost/gil/extension/io/png.hpp>
#include <boost/gil/extension/io/tiff.hpp>

int main() {
    boost::gil::rgb8_image_t img(100, 100);
    auto view = boost::gil::view(img);
    std::cout << "Boost GIL test package" << std::endl;
    return 0;
}