from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostFilesystemConan(ConanFile):
    name = "boost-filesystem"
    description = "Provides portable facilities to query and manipulate paths, files, and directories"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "system", "time")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "no_deprecated": [True, False],
        "disable_sendfile": [True, False],
        "disable_copy_file_range": [True, False],
        "disable_statx": [True, False],
        "disable_getrandom": [True, False],
        "disable_arc4random": [True, False],
        "disable_bcrypt": [True, False],
        "usa_wasi": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "no_deprecated": False,
        "disable_sendfile": False,
        "disable_copy_file_range": False,
        "disable_statx": False,
        "disable_getrandom": False,
        "disable_arc4random": False,
        "disable_bcrypt": False,
        "usa_wasi": False,
    }
    options_description = {
        "shared": "Build shared libraries",
        "fPIC": "Enable position independent code",
        "no_deprecated": "Disable deprecated functionality of Boost.Filesystem",
        "disable_sendfile": "Disable usage of sendfile API in Boost.Filesystem",
        "disable_copy_file_range": "Disable usage of copy_file_range API in Boost.Filesystem",
        "disable_statx": "Disable usage of statx API in Boost.Filesystem",
        "disable_getrandom": "Disable usage of getrandom API in Boost.Filesystem",
        "disable_arc4random": "Disable usage of arc4random API in Boost.Filesystem",
        "disable_bcrypt": "Disable usage of BCrypt API in Boost.Filesystem",
        "usa_wasi": "Use WASI under emscripten in Boost.Filesystem"
    }

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        else:
            del self.options.disable_bcrypt

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        # transitive headers: boost/filesystem/config.hpp:19:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem/path.hpp:29:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem/path.hpp:33:#include <boost/functional/hash_fwd.hpp>
        self.requires(f"boost-container-hash/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem/directory.hpp:29:#include <boost/detail/bitmask.hpp>
        self.requires(f"boost-detail/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem/path.hpp:32:#include <boost/io/quoted.hpp>
        self.requires(f"boost-io/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem/path.hpp:30:#include <boost/iterator/iterator_facade.hpp>
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem/exception.hpp:20:#include <boost/smart_ptr/intrusive_ptr.hpp>
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem.hpp:16:#include <boost/filesystem/path.hpp>
        self.requires(f"boost-system/{self.version}", transitive_headers=True)
        # transitive headers: boost/filesystem/detail/type_traits/disjunction.hpp:35:#include <boost/type_traits/disjunction.hpp>
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)

        self.requires(f"boost-core/{self.version}")
        self.requires(f"boost-atomic/{self.version}")
        self.requires(f"boost-predef/{self.version}")
        self.requires(f"boost-scope/{self.version}")
        if self.settings.os == "Windows":
            self.requires(f"boost-winapi/{self.version}")

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
        tc.cache_variables["CMAKE_PROJECT_BoostFilesystem_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BOOST_FILESYSTEM_NO_DEPRECATED"] = self.options.no_deprecated
        tc.cache_variables["BOOST_FILESYSTEM_DISABLE_SENDFILE"] = self.options.disable_sendfile
        tc.cache_variables["BOOST_FILESYSTEM_DISABLE_COPY_FILE_RANGE"] = self.options.disable_copy_file_range
        tc.cache_variables["BOOST_FILESYSTEM_DISABLE_STATX"] = self.options.disable_statx
        tc.cache_variables["BOOST_FILESYSTEM_DISABLE_GETRANDOM"] = self.options.disable_getrandom
        tc.cache_variables["BOOST_FILESYSTEM_DISABLE_ARC4RANDOM"] = self.options.disable_arc4random
        tc.cache_variables["BOOST_FILESYSTEM_EMSCRIPTEN_USE_WASI"] = self.options.usa_wasi
        if self.settings.os == "Windows":
            tc.cache_variables["BOOST_FILESYSTEM_DISABLE_BCRYPT"] = self.options.disable_bcrypt
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
        self.cpp_info.set_property("cmake_file_name", "boost_filesystem")
        self.cpp_info.set_property("cmake_target_name", "Boost::filesystem")
        self.cpp_info.libs = ["boost_filesystem"]
        if self.settings.os in ["Windows"]:
            self.cpp_info.system_libs = ["advapi32"]
            if not self.options.bcrypt:
                self.cpp_info.system_libs.append("bcrypt")
        self.cpp_info.defines = [
            "BOOST_FILESYSTEM_NO_LIB",
            "BOOST_FILESYSTEM_DYN_LINK" if self.options.shared else "BOOST_FILESYSTEM_STATIC_LINK"]
        if self.options.no_deprecated:
            self.cpp_info.defines.append("BOOST_FILESYSTEM_NO_DEPRECATED")