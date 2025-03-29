from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
import os


required_conan_version = ">=2.4"


class BoostSerializationConan(ConanFile):
    name = "boost-serialization"
    description = "Serialization for persistence and marshalling"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "io")
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
        self.requires(f"boost-array/{self.version}", transitive_headers=True)
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        self.requires(f"boost-detail/{self.version}", transitive_headers=True)
        self.requires(f"boost-integer/{self.version}", transitive_headers=True)
        self.requires(f"boost-io/{self.version}", transitive_headers=True)
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        self.requires(f"boost-move/{self.version}", transitive_headers=True)
        self.requires(f"boost-mpl/{self.version}", transitive_headers=True)
        self.requires(f"boost-optional/{self.version}", transitive_headers=True)
        self.requires(f"boost-predef/{self.version}", transitive_headers=True)
        self.requires(f"boost-preprocessor/{self.version}", transitive_headers=True)
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        self.requires(f"boost-spirit/{self.version}", transitive_headers=True)
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)
        self.requires(f"boost-variant/{self.version}", transitive_headers=True)
        self.requires(f"boost-mp11/{self.version}", transitive_headers=True)
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        self.requires(f"boost-variant2/{self.version}", transitive_headers=True)
        self.requires(f"boost-function/{self.version}")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_serialization_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_serialization")
        for component in ["serialization", "wserialization"]:
            self.cpp_info.components[component].set_property("cmake_target_name", f"Boost::{component}")
            self.cpp_info.components[component].libs = [f"boost_{component}"]
            self.cpp_info.components[component].defines = [
                "BOOST_SERIALIZATION_NO_LIB",
                "BOOST_SERIALIZATION_DYN_LINK" if self.options.shared else "BOOST_SERIALIZATION_STATIC_LINK"]
            self.cpp_info.components[component].requires = ["boost-headers::boost-headers", "boost-config::boost-config",
                "boost-array::boost-array", "boost-function::boost-function",
                "boost-core::boost-core", "boost-detail::boost-detail",
                "boost-integer::boost-integer", "boost-io::boost-io",
                "boost-iterator::boost-iterator", "boost-move::boost-move",
                "boost-mpl::boost-mpl", "boost-optional::boost-optional",
                "boost-predef::boost-predef", "boost-preprocessor::boost-preprocessor",
                "boost-smart-ptr::boost-smart-ptr", "boost-spirit::boost-spirit",
                "boost-static-assert::boost-static-assert",
                "boost-type-traits::boost-type-traits",
                "boost-utility::boost-utility", "boost-variant::boost-variant",]
        self.cpp_info.components["wserialization"].requires.append("serialization")
