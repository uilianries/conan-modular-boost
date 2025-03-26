from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostLocaleConan(ConanFile):
    name = "boost-locale"
    description = "Provide localization and Unicode handling tools for C++"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "string", "localization", "unicode")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_icu": [True, False],
        "enable_iconv": [True, False],
        "enable_posix": [True, False],
        "enable_std": [True, False],
        "enable_winapi": [True, False],
        }
    default_options = {
        "shared": False,
        "fPIC": True,
        "enable_icu": True,
        "enable_iconv": True,
        "enable_posix": True,
        "enable_std": True,
        "enable_winapi": True,
        }

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.enable_posix
            del self.options.fPIC
        if self.settings.os != "Windows":
            del self.options.enable_winapi
    
    def requirements(self):
        self.requires(f"boost-headers/{self.version}", transitive_headers=True)
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)

        self.requires(f"boost-predef/{self.version}")
        self.requires(f"boost-thread/{self.version}")

        if self.options.enable_icu:
            self.requires("icu/76.1")
        if self.options.enable_iconv:
            self.requires("libiconv/1.17")

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
        tc.cache_variables["CMAKE_PROJECT_boost_locale_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BOOST_LOCALE_ENABLE_ICU"] = self.options.enable_icu
        tc.cache_variables["BOOST_LOCALE_ENABLE_ICONV"] = self.options.enable_iconv
        tc.cache_variables["BOOST_LOCALE_ENABLE_POSIX"] = self.options.get_safe("enable_posix", False)
        tc.cache_variables["BOOST_LOCALE_ENABLE_STD"] = self.options.enable_std
        tc.cache_variables["BOOST_LOCALE_ENABLE_WINAPI"] = self.options.get_safe("enable_winapi", False)
        tc.cache_variables["BOOST_LOCALE_WERROR"] = False
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
        self.cpp_info.set_property("cmake_file_name", "boost_locale")
        self.cpp_info.set_property("cmake_target_name", "Boost::locale")
        self.cpp_info.libs = ["boost_locale"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs = ["pthread"]
        self.cpp_info.defines = [
            "BOOST_LOCALE_NO_LIB",
            "BOOST_LOCALE_DYN_LINK" if self.options.shared else "BOOST_LOCALE_STATIC_LINK"]
