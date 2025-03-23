from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostTestConan(ConanFile):
    name = "boost-test"
    description = "Support for simple program testing, full unit testing, and for program execution monitoring"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "correctness", "testing")
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
        # transitive headers: boost/test/utils/timer.hpp:14:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/utils/runtime/parameter.hpp:31:#include <boost/algorithm/cxx11/all_of.hpp>
        self.requires(f"boost-algorithm/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/tools/floating_point_comparison.hpp:22:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/impl/framework.ipp:52:#include <boost/bind/bind.hpp>
        self.requires(f"boost-bind/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/impl/debug.ipp:25:#include <boost/core/ignore_unused.hpp>
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/detail/config.hpp:17:#include <boost/detail/workaround.hpp>
        self.requires(f"boost-detail/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/impl/execution_monitor.ipp:35:#include <boost/exception/get_error_info.hpp>
        self.requires(f"boost-exception/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/debug.hpp:22:#include <boost/function/function1.hpp>
        self.requires(f"boost-function/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/impl/unit_test_log.ipp:34:#include <boost/io/ios_state.hpp>
        self.requires(f"boost-io/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/utils/iterator/token_iterator.hpp:23:#include <boost/iterator/iterator_traits.hpp>
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/tools/assertion.hpp:23:#include <boost/mpl/assert.hpp>
        self.requires(f"boost-mpl/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/tools/old/impl.hpp:28:#include <boost/numeric/conversion/conversion_traits.hpp>
        self.requires(f"boost-numeric-conversion/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/data/monomorphic/generators/xrange.hpp:22:#include <boost/optional.hpp>
        self.requires(f"boost-optional/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/data/test_case.hpp:28:#include <boost/preprocessor/cat.hpp>
        self.requires(f"boost-preprocessor/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/tools/detail/indirections.hpp:24:#include <boost/shared_ptr.hpp>
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/utils/is_forward_iterable.hpp:38:#include <boost/static_assert.hpp>
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/utils/class_properties.hpp:28:#include <boost/type_traits/add_const.hpp>
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        # transitive headers: boost/test/tools/assertion.hpp:24:#include <boost/utility/declval.hpp>
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)

        self.requires(f"boost-describe/{self.version}")

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
        tc.cache_variables["CMAKE_PROJECT_boost_test_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
            # INFO: test_exec_monitor is static only
            copy(self, "libboost_test_exec_monitor.*", self.build_folder, os.path.join(self.package_folder, "lib"))
            copy(self, "boost_test_exec_monitor.lib", self.build_folder, os.path.join(self.package_folder, "lib"))
        else:
            copy(self, "*.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "boost_test")
        self.cpp_info.set_property("cmake_target_name", "Boost::test")

        for component in ["prg_exec_monitor", "unit_test_framework", "test_exec_monitor"]:
            self.cpp_info.components[component].set_property("cmake_file_name", f"boost_{component}")
            self.cpp_info.components[component].set_property("cmake_target_name", f"Boost::{component}")
            self.cpp_info.components[component].libs = [f"boost_{component}"]
            self.cpp_info.components[component].defines = [
                "BOOST_TEST_NO_LIB",
                "BOOST_TEST_DYN_LINK" if self.options.shared else "BOOST_TEST_STATIC_LINK"]
            self.cpp_info.components[component].requires = [
                "boost-headers::boost-headers",
                "boost-config::boost-config",
                "boost-algorithm::boost-algorithm",
                "boost-assert::boost-assert",
                "boost-bind::boost-bind",
                "boost-core::boost-core",
                "boost-detail::boost-detail",
                "boost-describe::boost-describe",
                "boost-exception::boost-exception",
                "boost-function::boost-function",
                "boost-io::boost-io",
                "boost-iterator::boost-iterator",
                "boost-mpl::boost-mpl",
                "boost-numeric-conversion::boost-numeric-conversion",
                "boost-optional::boost-optional",
                "boost-preprocessor::boost-preprocessor",
                "boost-smart-ptr::boost-smart-ptr",
                "boost-static-assert::boost-static-assert",
                "boost-type-traits::boost-type-traits",
                "boost-utility::boost-utility"]
