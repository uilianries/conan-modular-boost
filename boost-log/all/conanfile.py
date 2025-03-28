from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostLogConan(ConanFile):
    name = "boost-log"
    description = "Logging library"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "miscellaneous", "logging")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires(f"boost-headers/{self.version}", transitive_headers=True)
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        self.requires(f"boost-date-time/{self.version}", transitive_headers=True)
        self.requires(f"boost-filesystem/{self.version}", transitive_headers=True)
        self.requires(f"boost-function-types/{self.version}", transitive_headers=True)
        self.requires(f"boost-fusion/{self.version}", transitive_headers=True)
        self.requires(f"boost-intrusive/{self.version}", transitive_headers=True)
        self.requires(f"boost-move/{self.version}", transitive_headers=True)
        self.requires(f"boost-mpl/{self.version}", transitive_headers=True)
        self.requires(f"boost-parameter/{self.version}", transitive_headers=True)
        self.requires(f"boost-phoenix/{self.version}", transitive_headers=True)
        self.requires(f"boost-predef/{self.version}", transitive_headers=True)
        self.requires(f"boost-preprocessor/{self.version}", transitive_headers=True)
        self.requires(f"boost-proto/{self.version}", transitive_headers=True)
        self.requires(f"boost-range/{self.version}", transitive_headers=True)
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        self.requires(f"boost-system/{self.version}", transitive_headers=True)
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        self.requires(f"boost-type-index/{self.version}", transitive_headers=True)
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)
        self.requires(f"boost-atomic/{self.version}", transitive_headers=True)
        self.requires(f"boost-thread/{self.version}", transitive_headers=True)
        self.requires(f"boost-winapi/{self.version}", transitive_headers=True)
        self.requires(f"boost-regex/{self.version}", transitive_headers=True)
        self.requires(f"boost-xpressive/{self.version}", transitive_headers=True)
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        self.requires(f"boost-property-tree/{self.version}", transitive_headers=True)

        self.requires(f"boost-align/{self.version}")
        self.requires(f"boost-asio/{self.version}")
        self.requires(f"boost-bind/{self.version}")
        self.requires(f"boost-exception/{self.version}")
        self.requires(f"boost-interprocess/{self.version}")
        self.requires(f"boost-io/{self.version}")
        self.requires(f"boost-optional/{self.version}")
        self.requires(f"boost-random/{self.version}")
        self.requires(f"boost-spirit/{self.version}")

        
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
        tc.cache_variables["CMAKE_PROJECT_BoostLog_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_log")
        self.cpp_info.components["log"].set_property("cmake_target_name", "Boost::log")
        self.cpp_info.components["log"].libs = ["boost_log"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.components["log"].system_libs = ["pthread", "rt"]
        elif self.settings.os == "Windows":
            self.cpp_info.components["log"].system_libs = ["psapi", "advapi32", "secur32", "ws2_32", "mswsock"]
        self.cpp_info.components["log"].defines = [
            "BOOST_LOG_NO_LIB",
            "BOOST_LOG_DYN_LINK" if self.options.shared else "BOOST_LOG_STATIC_LINK"]
        self.cpp_info.components["log"].requires = [
            "boost-headers::boost-headers",
            "boost-assert::boost-assert",
            "boost-config::boost-config",
            "boost-core::boost-core",
            "boost-date-time::boost-date-time",
            "boost-filesystem::boost-filesystem",
            "boost-function-types::boost-function-types",
            "boost-fusion::boost-fusion",
            "boost-intrusive::boost-intrusive",
            "boost-move::boost-move",
            "boost-mpl::boost-mpl",
            "boost-parameter::boost-parameter",
            "boost-phoenix::boost-phoenix",
            "boost-predef::boost-predef",
            "boost-preprocessor::boost-preprocessor",
            "boost-proto::boost-proto",
            "boost-range::boost-range",
            "boost-smart-ptr::boost-smart-ptr",
            "boost-system::boost-system",
            "boost-throw-exception::boost-throw-exception",
            "boost-type-index::boost-type-index",
            "boost-type-traits::boost-type-traits",
            "boost-utility::boost-utility",
            "boost-align::boost-align",
            "boost-asio::boost-asio",
            "boost-bind::boost-bind",
            "boost-exception::boost-exception",
            "boost-interprocess::boost-interprocess",
            "boost-optional::boost-optional",
            "boost-random::boost-random",
            "boost-spirit::boost-spirit",
            "boost-regex::boost-regex",
            "boost-xpressive::boost-xpressive",
            "boost-winapi::boost-winapi",
            "boost-atomic::boost-atomic",
            "boost-thread::boost-thread",
        ]
        self.cpp_info.components["log_setup"].set_property("cmake_target_name", "Boost::log_setup")
        self.cpp_info.components["log_setup"].libs = ["boost_log_setup"]
        self.cpp_info.components["log_setup"].requires = [
            "log",
            "boost-headers::boost-headers",
            "boost-assert::boost-assert",
            "boost-config::boost-config",
            "boost-core::boost-core",
            "boost-iterator::boost-iterator",
            "boost-optional::boost-optional",
            "boost-parameter::boost-parameter",
            "boost-phoenix::boost-phoenix",
            "boost-preprocessor::boost-preprocessor",
            "boost-property-tree::boost-property-tree",
            "boost-smart-ptr::boost-smart-ptr",
            "boost-type-traits::boost-type-traits",
            "boost-asio::boost-asio",
            "boost-bind::boost-bind",
            "boost-date-time::boost-date-time",
            "boost-exception::boost-exception",
            "boost-filesystem::boost-filesystem",
            "boost-io::boost-io",
            "boost-spirit::boost-spirit",
            "boost-throw-exception::boost-throw-exception",
            "boost-utility::boost-utility",
            "boost-fusion::boost-fusion",
            "boost-mpl::boost-mpl",
            "boost-regex::boost-regex",
            "boost-xpressive::boost-xpressive",
        ]
        self.cpp_info.components["log_setup"].defines = [
            "BOOST_LOG_NO_LIB",
            "BOOST_LOG_DYN_LINK" if self.options.shared else "BOOST_LOG_STATIC_LINK"]
        
        self.cpp_info.components["log_with_support"].set_property("cmake_target_name", "Boost::log_with_support")
        self.cpp_info.components["log_with_support"].requires = [
            "log",
            "boost-headers::boost-headers",
            "boost-config::boost-config",
            "boost-exception::boost-exception",
            "boost-regex::boost-regex",
            "boost-spirit::boost-spirit",
            "boost-xpressive::boost-xpressive",
        ]
        self.cpp_info.components["log_with_support"].bindirs = []
        self.cpp_info.components["log_with_support"].libdirs = []
        self.cpp_info.components["log_with_support"].includedirs = []