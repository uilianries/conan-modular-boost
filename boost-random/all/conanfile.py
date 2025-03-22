from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostRandomConan(ConanFile):
    name = "boost-random"
    description = "A complete system for random number generation"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "math")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        # transitive headers: boost/random/shuffle_order.hpp:21:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/sobol.hpp:14:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/hyperexponential_distribution.hpp:23:#include <boost/core/cmath.hpp>
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/niederreiter_base2.hpp:15:#include <boost/dynamic_bitset.hpp>
        self.requires(f"boost-dynamic-bitset/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/detail/int_float_pair.hpp:19:#include <boost/integer.hpp>
        self.requires(f"boost-integer/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/detail/vector_io.hpp:19:#include <boost/io/ios_state.hpp>
        self.requires(f"boost-io/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/shuffle_order.hpp:23:#include <boost/static_assert.hpp>
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/random_device.hpp:25:#include <boost/system/config.hpp>
        self.requires(f"boost-system/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/detail/gray_coded_qrng.hpp:15:#include <boost/throw_exception.hpp>
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/uniform_real_distribution.hpp:26:#include <boost/type_traits/is_integral.hpp>
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/subtract_with_carry.hpp:29:#include <boost/detail/workaround.hpp>
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/mixmax.hpp:22:#include <boost/array.hpp>
        self.requires(f"boost-array/{self.version}", transitive_headers=True)
        # transitive headers: boost/random/seed_seq.hpp:19:#include <boost/range/begin.hpp>
        self.requires(f"boost-range/{self.version}", transitive_headers=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        check_min_cppstd(self, "11")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_random_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BUILD_TESTING"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE_1_0.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, "*.hpp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.h", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.ipp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        if self.options.shared:
            copy(self, "*.so*", self.build_folder, os.path.join(self.package_folder, "lib"))
            copy(self, "*.dylib*", self.build_folder, os.path.join(self.package_folder, "lib"))
            copy(self, "*.dll", self.build_folder, os.path.join(self.package_folder, "bin"))
            copy(self, "*.dll.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        else:
            copy(self, "*.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))


    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "boost_random")
        self.cpp_info.set_property("cmake_target_name", "Boost::random")
        self.cpp_info.libs = ["boost_random"]
        self.cpp_info.defines = [
            "BOOST_RANDOM_NO_LIB",
            "BOOST_RANDOM_DYN_LINK" if self.options.shared else "BOOST_RANDOM_STATIC_LINK"]
