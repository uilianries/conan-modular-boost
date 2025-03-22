from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostFiberConan(ConanFile):
    name = "boost-fiber"
    description = "(C++11) Userland threads library"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "concurrent", "system")
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
        # transitive headers: boost/fiber/operations.hpp:11:#include <boost/config.hpp> 
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/fiber/mutex.hpp:12:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/fiber/detail/disable_overload.hpp:13:#include <boost/context/detail/disable_overload.hpp>
        self.requires(f"boost-context/{self.version}", transitive_headers=True)
        # transitive headers: boost/fiber/future/promise.hpp:15:#include <boost/core/pointer_traits.hpp>
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/fiber/scheduler.hpp:17:#include <boost/intrusive/list.hpp>
        self.requires(f"boost-intrusive/{self.version}", transitive_headers=True)
        # transitive headers: boost/fiber/fiber.hpp:18:#include <boost/predef.h>
        self.requires(f"boost-predef/{self.version}", transitive_headers=True)
        # transitive headers: boost/fiber/fiber.hpp:17:#include <boost/intrusive_ptr.hpp>
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        
        self.requires(f"boost-algorithm/{self.version}")
        self.requires(f"boost-filesystem/{self.version}")
        self.requires(f"boost-format/{self.version}")

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
        tc.cache_variables["CMAKE_PROJECT_boost_fiber_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_fiber")
        
        self.cpp_info.components["fiber"].set_property("cmake_target_name", "Boost::fiber")
        self.cpp_info.components["fiber"].libs = ["boost_fiber"]
        self.cpp_info.components["fiber"].defines = [
            "BOOST_FIBER_NO_LIB",
            "BOOST_FIBER_DYN_LINK" if self.options.shared else "BOOST_FIBER_STATIC_LINK"]
        self.cpp_info.components["fiber"].requires = [
            "boost-headers::boost-headers",
            "boost-config::boost-config",
            "boost-assert::boost-assert",
            "boost-context::boost-context",
            "boost-core::boost-core",
            "boost-intrusive::boost-intrusive",
            "boost-predef::boost-predef",
            "boost-smart-ptr::boost-smart-ptr",
        ]            
        self.cpp_info.components["fiber_numa"].set_property("cmake_target_name", "Boost::fiber_numa")
        self.cpp_info.components["fiber_numa"].libs = ["boost_fiber_numa"]
        self.cpp_info.components["fiber_numa"].requires = [
            "fiber",
            "boost-headers::boost-headers",
            "boost-config::boost-config",
            "boost-assert::boost-assert",
            "boost-context::boost-context",
            "boost-smart-ptr::boost-smart-ptr",
            "boost-algorithm::boost-algorithm",
            "boost-filesystem::boost-filesystem",
            "boost-format::boost-format",
        ]