from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostProgramOptionsConan(ConanFile):
    name = "boost-program-options"
    description = "Allows program developers to obtain program options"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "miscellaneous", "time")
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
        # transitive headers: boost/program_options/config.hpp:10:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/options_description.hpp:18:#include <boost/any.hpp>
        self.requires(f"boost-any/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/detail/config_file.hpp:14:#include <boost/noncopyable.hpp>
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/options_description.hpp:17:#include <boost/detail/workaround.hpp>
        self.requires(f"boost-detail/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/value_semantic.hpp:13:#include <boost/function/function1.hpp>
        self.requires(f"boost-function/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/eof_iterator.hpp:9:#include <boost/iterator/iterator_facade.hpp>
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/value_semantic.hpp:14:#include <boost/lexical_cast.hpp>
        self.requires(f"boost-lexical-cast/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/detail/config_file.hpp:28:#include <boost/shared_ptr.hpp>
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/detail/config_file.hpp:26:#include <boost/static_assert.hpp>
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/detail/value_semantic.hpp:9:#include <boost/throw_exception.hpp>
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        # transitive headers: boost/program_options/detail/config_file.hpp:27:#include <boost/type_traits/is_same.hpp>
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)

        self.requires(f"boost-bind/{self.version}")
        self.requires(f"boost-tokenizer/{self.version}")
    
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
        tc.cache_variables["CMAKE_PROJECT_boost_program_options_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_program_options")
        self.cpp_info.set_property("cmake_target_name", "Boost::program_options")
        self.cpp_info.libs = ["boost_program_options"]
        self.cpp_info.defines = [
            "BOOST_PROGRAM_OPTIONS_NO_LIB",
            "BOOST_PROGRAM_OPTIONS_DYN_LINK" if self.options.shared else "BOOST_PROGRAM_OPTIONS_STATIC_LINK"]
