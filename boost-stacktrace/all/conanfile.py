from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.microsoft import is_msvc
from conan.tools.apple import is_apple_os
import os


required_conan_version = ">=2.4"


class BoostTimerConan(ConanFile):
    name = "boost-stacktrace"
    description = "Gather, store, copy and print backtraces"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "correctness", "system")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_noop": [True, False],
        "enable_backtrace": [True, False],
        "enable_addr2line": [True, False],
        "enable_basic": [True, False],
        "enable_windbg": [True, False],
        "enable_windbg_cached": [True, False],
        "enable_from_exception": [True, False]
        }
    default_options = {
        "shared": False,
        "fPIC": True,
        "enable_noop": True,
        "enable_backtrace": True,
        "enable_addr2line": True,
        "enable_basic": True,
        "enable_windbg": True,
        "enable_windbg_cached": True,
        "enable_from_exception": True
        }

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if is_msvc(self):
            del self.options.enable_addr2line
        if self.settings.os == "Windows":
            del self.options.fPIC
        else:
            del self.options.enable_windbg
            del self.options.enable_windbg_cached
        if "x86" not in str(self.settings.arch) and "arm" not in str(self.settings.arch):
            self.options.enable_from_exception = False

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        # transitive headers: boost/stacktrace.hpp:10
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/stacktrace/stacktrace.hpp:16
        self.requires(f"boost-container-hash/{self.version}", transitive_headers=True)
        # transitive headers: stacktrace/stacktrace.hpp:15
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/stacktrace/detail/collect_unwind.ipp:19
        self.requires(f"boost-predef/{self.version}", transitive_headers=True)
        # transitive headers: boost/stacktrace/safe_dump_to.hpp:18
        self.requires(f"boost-winapi/{self.version}", transitive_headers=True)
        if self.options.enable_backtrace:
            # transitive headers: boost/stacktrace/detail/libbacktrace_impls.hpp:23
            self.requires("libbacktrace/cci.20240730", transitive_headers=True)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])
        # FIXME: The check_cxx_source_compiles is used to find backtrace, but lacks header and library folder
        # This workaround enforce to use the CMake target for libbacktrace without patching the source
        # It replaces the CMake file for testing and mark build testing as enabled
        copy(self, "CMakeLists.txt", src=self.export_sources_folder, dst=os.path.join(self.source_folder, "test"))

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_stacktrace_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BOOST_STACKTRACE_ENABLE_BACKTRACE"] = self.options.enable_backtrace
        tc.cache_variables["BOOST_STACKTRACE_ENABLE_ADDR2LINE"] = self.options.get_safe("enable_addr2line", False)
        tc.cache_variables["BOOST_STACKTRACE_ENABLE_NOOP"] = self.options.enable_noop
        tc.cache_variables["BOOST_STACKTRACE_ENABLE_BASIC"] = self.options.enable_basic
        tc.cache_variables["BOOST_STACKTRACE_ENABLE_FROM_EXCEPTION"] = self.options.enable_from_exception
        tc.cache_variables["BUILD_TESTING"] = self.options.enable_backtrace
        if self.settings.os == "Windows":
            tc.cache_variables["BOOST_STACKTRACE_ENABLE_WINDBG"] = self.options.enable_windbg
            tc.cache_variables["BOOST_STACKTRACE_ENABLE_WINDBG_CACHED"] = self.options.enable_windbg_cached
        if self.options.get_safe("enable_addr2line", False):
            addr2line_path = os.path.join(self.dependencies["libbacktrace"].cpp_info.bindir, "addr2line").replace("\\", "/")
            tc.preprocessor_definitions["BOOST_STACKTRACE_ADDR2LINE_LOCATION"] = addr2line_path
        if "x86" not in str(self.settings.arch) and self.options.enable_from_exception:
            # https://github.com/boostorg/stacktrace/blob/develop/src/from_exception.cpp#L171
            # This feature is guarded by BOOST_STACKTRACE_ALWAYS_STORE_IN_PADDING, but that is only enabled on x86.
            tc.preprocessor_definitions["BOOST_STACKTRACE_LIBCXX_RUNTIME_MAY_CAUSE_MEMORY_LEAK"] = "1"
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE_1_0.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, "*.h", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.hpp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
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
        self.cpp_info.set_property("cmake_file_name", "boost_stacktrace")
        self.cpp_info.set_property("cmake_target_name", "Boost::stacktrace")
        for component in ["addr2line", "backtrace", "basic", "noop", "windbg", "windbg_cached", "from_exception"]:
            if component in ["windbg", "windbg_cached"] and self.settings.os != "Windows":
                continue
            if not self.options.get_safe(f"enable_{component}"):
                continue
            self.cpp_info.components[component].set_property("cmake_target_name", f"Boost::stacktrace_{component}")
            self.cpp_info.components[component].libs = [f"boost_stacktrace_{component}"]
            self.cpp_info.components[component].requires = [
                "boost-headers::boost-headers",
                "boost-config::boost-config",
                "boost-container-hash::boost-container-hash",
                "boost-core::boost-core",
                "boost-predef::boost-predef",
                "boost-winapi::boost-winapi",
                ]
            self.cpp_info.components[component].defines = [
                "BOOST_STACKTRACE_NO_LIB",
                "BOOST_STACKTRACE_DYN_LINK" if self.options.shared else "BOOST_STACKTRACE_STATIC_LINK"]
            if component == "backtrace":
                self.cpp_info.components[component].requires.append("libbacktrace::libbacktrace")
                self.cpp_info.components[component].defines.append("BOOST_STACKTRACE_USE_BACKTRACE")
            elif component == "addr2line":
                self.cpp_info.components[component].defines.append("BOOST_STACKTRACE_USE_ADDR2LINE")
            elif component == "noop":
                self.cpp_info.components[component].defines.append("BOOST_STACKTRACE_USE_NOOP")
            elif component == "windbg":
                self.cpp_info.components[component].defines.append("BOOST_STACKTRACE_USE_WINDBG")
            elif component == "windbg_cached":
                self.cpp_info.components[component].defines.append("BOOST_STACKTRACE_USE_WINDBG_CACHED")
            if component in ["basic", "addr2line", "backtrace"] and self.settings.os == "Linux":
                self.cpp_info.components[component].system_libs = ["dl"]
            elif component in ["windbg", "windbg_cached"] and self.settings.os == "Windows":
                self.cpp_info.components[component].system_libs = ["dbgeng", "ole32"]
                self.cpp_info.components[component].defines.append("_GNU_SOURCE=1")
