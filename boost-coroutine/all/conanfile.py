from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
import os


required_conan_version = ">=2.4"


class BoostCoroutineConan(ConanFile):
    name = "boost-coroutine"
    description = "Coroutine library"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "concurrent", "time")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {"shared": [True, False], "fPIC": [True, False], "use_segmented_stacks": [True, False]}
    default_options = {"shared": False, "fPIC": True, "use_segmented_stacks": False}

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        # transitive headers: boost/coroutine/stack_context.hpp:12:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/posix/protected_stack_allocator.hpp:25:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/detail/push_coroutine_object.hpp:12:#include <boost/context/detail/config.hpp>
        self.requires(f"boost-context/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/exceptions.hpp:14:#include <boost/core/scoped_enum.hpp>
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/detail/trampoline_push.hpp:16:#include <boost/exception_ptr.hpp>
        self.requires(f"boost-exception/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/detail/symmetric_coroutine_yield.hpp:14:#include <boost/move/move.hpp>
        self.requires(f"boost-move/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/exceptions.hpp:15:#include <boost/system/error_code.hpp>
        self.requires(f"boost-system/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/asymmetric_coroutine.hpp:17:#include <boost/throw_exception.hpp>
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/detail/setup.hpp:15:#include <boost/type_traits/is_same.hpp>
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        # transitive headers: boost/coroutine/detail/pull_coroutine_impl.hpp:14:#include <boost/utility.hpp>
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_coroutine_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_coroutine")
        self.cpp_info.set_property("cmake_target_name", "Boost::coroutine")
        self.cpp_info.libs = ["boost_coroutine"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs = ["pthread"]
        # INFO: Boost Coroutine has duplicated/messed defines: COROUTINE COUROUTINES
        self.cpp_info.defines = [
            "BOOST_COROUTINE_NO_LIB", "BOOST_COROUTINES_NO_LIB",
            "BOOST_COROUTINE_DYN_LINK" if self.options.shared else "BOOST_COROUTINE_STATIC_LINK",
            "BOOST_COROUTINES_DYN_LINK" if self.options.shared else "BOOST_COROUTINES_STATIC_LINK"]
        if self.options.use_segmented_stacks:
            self.cpp_info.defines.append("BOOST_USE_SEGMENTED_STACKS=1")
