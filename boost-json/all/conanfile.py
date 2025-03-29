from conan import ConanFile
from conan.tools.files import copy, get, download, replace_in_file
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostJsonConan(ConanFile):
    name = "boost-json"
    description = "JSON parsing, serialization, and DOM in C++11"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "containers", "data", "io", "time")
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
        # transitive headers: boost/json/detail/charconv/limits.hpp:8
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/impl/static_resource.ipp:15
        self.requires(f"boost-align/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/detail/config.hpp:15
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/static_resource.hpp:13
        self.requires(f"boost-container/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/impl/object.ipp:13
        self.requires(f"boost-container-hash/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/string_view.hpp:14
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/detail/value_to.hpp:18
        self.requires(f"boost-describe/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/detail/utf8.hpp:13
        self.requires(f"boost-endian/{self.version}", transitive_headers=True)
        # transitive headers: json/detail/stack.hpp:15
        self.requires(f"boost-mp11/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/result_for.hpp:17
        self.requires(f"boost-system/{self.version}", transitive_headers=True)
        # transitive headers: boost/json/detail/impl/except.ipp:15
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        check_min_cppstd(self, "11")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])
        # INFO: Do not try to include other boost libraries as subdirectories
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "add_subdirectory(../.. _deps/boost EXCLUDE_FROM_ALL)", "")

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_json_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BOOST_JSON_BUILD_TESTS"] = False
        tc.cache_variables["BOOST_JSON_BUILD_FUZZERS"] = False
        tc.cache_variables["BOOST_JSON_BUILD_EXAMPLES"] = False
        tc.cache_variables["BOOST_JSON_BUILD_BENCHMARKS"] = False
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
        self.cpp_info.set_property("cmake_file_name", "boost_json")
        self.cpp_info.set_property("cmake_target_name", "Boost::json")
        self.cpp_info.libs = ["boost_json"]
        self.cpp_info.defines = [
            "BOOST_JSON_NO_LIB",
            "BOOST_JSON_DYN_LINK" if self.options.shared else "BOOST_JSON_STATIC_LINK"]
