from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostGraphConan(ConanFile):
    name = "boost-graph"
    description = "The BGL graph interface and graph components are generic, in the same sense as the STL"
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
        self.requires(f"boost-headers/{self.version}", transitive_headers=True)
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        self.requires(f"boost-algorithm/{self.version}", transitive_headers=True)
        self.requires(f"boost-any/{self.version}", transitive_headers=True)
        self.requires(f"boost-array/{self.version}", transitive_headers=True)
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-bimap/{self.version}", transitive_headers=True)
        self.requires(f"boost-bind/{self.version}", transitive_headers=True)
        self.requires(f"boost-concept-check/{self.version}", transitive_headers=True)
        self.requires(f"boost-container-hash/{self.version}", transitive_headers=True)
        self.requires(f"boost-conversion/{self.version}", transitive_headers=True)
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        self.requires(f"boost-detail/{self.version}", transitive_headers=True)
        self.requires(f"boost-foreach/{self.version}", transitive_headers=True)
        self.requires(f"boost-function/{self.version}", transitive_headers=True)
        self.requires(f"boost-integer/{self.version}", transitive_headers=True)
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        self.requires(f"boost-lexical-cast/{self.version}", transitive_headers=True)
        self.requires(f"boost-math/{self.version}", transitive_headers=True)
        self.requires(f"boost-move/{self.version}", transitive_headers=True)
        self.requires(f"boost-mpl/{self.version}", transitive_headers=True)
        self.requires(f"boost-multi-index/{self.version}", transitive_headers=True)
        self.requires(f"boost-optional/{self.version}", transitive_headers=True)
        self.requires(f"boost-parameter/{self.version}", transitive_headers=True)
        self.requires(f"boost-preprocessor/{self.version}", transitive_headers=True)
        self.requires(f"boost-property-map/{self.version}", transitive_headers=True)
        self.requires(f"boost-property-tree/{self.version}", transitive_headers=True)
        self.requires(f"boost-random/{self.version}", transitive_headers=True)
        self.requires(f"boost-range/{self.version}", transitive_headers=True)
        self.requires(f"boost-serialization/{self.version}", transitive_headers=True)
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        self.requires(f"boost-spirit/{self.version}", transitive_headers=True)
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        self.requires(f"boost-tti/{self.version}", transitive_headers=True)
        self.requires(f"boost-tuple/{self.version}", transitive_headers=True)
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        self.requires(f"boost-typeof/{self.version}", transitive_headers=True)
        self.requires(f"boost-unordered/{self.version}", transitive_headers=True)
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)
        self.requires(f"boost-xpressive/{self.version}", transitive_headers=True)
        self.requires(f"boost-regex/{self.version}")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        check_min_cppstd(self, "14")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_graph_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
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
        self.cpp_info.set_property("cmake_file_name", "boost_graph")
        self.cpp_info.set_property("cmake_target_name", "Boost::graph")
        self.cpp_info.libs = ["boost_graph"]
        self.cpp_info.defines = [
            "BOOST_GRAPH_NO_LIB",
            "BOOST_GRAPH_DYN_LINK" if self.options.shared else "BOOST_GRAPH_STATIC_LINK"]
