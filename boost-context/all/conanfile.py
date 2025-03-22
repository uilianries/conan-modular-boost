from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostContextConan(ConanFile):
    name = "boost-context"
    description = "(C++11) Context switching library"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "concurrent", "system")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {"shared": [True, False], "fPIC": [True, False], "implementation": ["fcontext", "ucontext", "winfib"]}
    default_options = {"shared": False, "fPIC": True, "implementation": "fcontext"}

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        # transitive headers: boost/context/stack_context.hpp:12
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/context/pooled_fixedsize_stack.hpp:15
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/context/posix/protected_fixedsize_stack.hpp:23
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/context/detail/index_sequence.hpp:17
        self.requires(f"boost-mp11/{self.version}", transitive_headers=True)
        # transitive headers: boost/context/pooled_fixedsize_stack.hpp:18
        self.requires(f"boost-pool/{self.version}", transitive_headers=True)
        # transitive headers: boost/context/detail/prefetch.hpp:13
        self.requires(f"boost-predef/{self.version}", transitive_headers=True)
        # transitive headers: boost/context/pooled_fixedsize_stack.hpp:17
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)

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
        tc.cache_variables["CMAKE_PROJECT_boost_context_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_context")
        self.cpp_info.set_property("cmake_target_name", "Boost::context")
        self.cpp_info.libs = ["boost_context"]
        self.cpp_info.defines = [
            "BOOST_CONTEXT_NO_LIB",
            "BOOST_CONTEXT_DYN_LINK" if self.options.shared else "BOOST_CONTEXT_STATIC_LINK"]
        if self.options.implementation == "ucontext":
            self.cpp_info.defines.append("BOOST_USE_UCONTEXT")
        elif self.options.implementation == "winfib":
            self.cpp_info.defines.append("BOOST_USE_WINFIB")
