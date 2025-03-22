from conan import ConanFile
from conan.tools.files import copy, get, download, replace_in_file
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostURLConan(ConanFile):
    name = "boost-url"
    description = "URL parsing in C++11"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "containers", "data", "io")
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
        # transitive headers: boost/url/detail/config.hpp:14
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/static_url.hpp:15
        self.requires(f"boost-align/{self.version}", transitive_headers=True)
        # transitive headers: include/boost/url/detail/url_impl.hpp:18
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/detail/encode.hpp:17
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/grammar/detail/tuple.hpp:17
        self.requires(f"boost-mp11/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/optional.hpp:14
        self.requires(f"boost-optional/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/error_types.hpp:14
        self.requires(f"boost-system/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/grammar/unsigned_rule.hpp:18
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/grammar/detail/tuple.hpp:20
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        # transitive headers: boost/url/variant.hpp:14
        self.requires(f"boost-variant2/{self.version}", transitive_headers=True)
        self.requires(f"boost-throw-exception/{self.version}")

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
        tc.cache_variables["CMAKE_PROJECT_boost_url_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BOOST_URL_BUILD_EXAMPLES"] = False
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):
        # There is no dedicated Boost cmake file for individual libraries
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "find_package(Boost REQUIRED COMPONENTS container)", "")

    def build(self):
        self._patch_sources()
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
        self.cpp_info.set_property("cmake_file_name", "boost_url")
        self.cpp_info.set_property("cmake_target_name", "Boost::url")
        self.cpp_info.libs = ["boost_url"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs = ["pthread"]
        self.cpp_info.defines = [
            "BOOST_URL_NO_LIB",
            "BOOST_URL_DYN_LINK" if self.options.shared else "BOOST_URL_STATIC_LINK"]
