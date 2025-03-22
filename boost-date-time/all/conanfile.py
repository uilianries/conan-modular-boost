from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
import os


required_conan_version = ">=2.4"


class BoostDateTimeConan(ConanFile):
    name = "boost-date-time"
    description = "A set of date-time libraries based on generic programming concepts"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "domain", "time")
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
        # transitive headers: boost/date_time/compiler_config.hpp:12:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/time_facet.hpp:25:#include <boost/algorithm/string/erase.hpp>
        self.requires(f"boost-algorithm/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/time_facet.hpp:21:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/time_duration.hpp:12:#include <boost/core/enable_if.hpp>
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/date_formatting.hpp:14:#include <boost/io/ios_state.hpp>
        self.requires(f"boost-io/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/time_facet.hpp:22:#include <boost/lexical_cast.hpp>
        self.requires(f"boost-lexical-cast/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/c_local_time_adjustor.hpp:20:#include <boost/numeric/conversion/cast.hpp>
        self.requires(f"boost-numeric-conversion/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/time_facet.hpp:24:#include <boost/range/as_literal.hpp>
        self.requires(f"boost-range/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/tz_db_base.hpp:18:#include <boost/shared_ptr.hpp>
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/time_duration.hpp:18:#include <boost/static_assert.hpp>
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/c_time.hpp:20:#include <boost/throw_exception.hpp>
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/date_parsing.hpp:17:#include <boost/tokenizer.hpp>
        self.requires(f"boost-tokenizer/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/constrained_value.hpp:17:#include <boost/type_traits/is_base_of.hpp>
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/compiler_config.hpp:13:#include <boost/detail/workaround.hpp>
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)
        # transitive headers: boost/date_time/microsec_time_clock.hpp:24:#include <boost/winapi/time.hpp>
        self.requires(f"boost-winapi/{self.version}", transitive_headers=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_date_time_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_date_time")
        self.cpp_info.set_property("cmake_target_name", "Boost::date_time")
        self.cpp_info.libs = ["boost_date_time"]
        self.cpp_info.defines = [
            "BOOST_DATE_TIME_NO_LIB",
            "BOOST_DATE_TIME_DYN_LINK" if self.options.shared else "BOOST_DATE_TIME_STATIC_LINK"]
