from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostgGeometryConan(ConanFile):
    name = "boost-geometry"
    description = "The Boost.Geometry library provides geometric algorithms, primitives and spatial index"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "algorithms", "data", "math", "header-only")
    package_type = "header-library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        self.requires(f"boost-config/{self.version}")
        self.requires(f"boost-algorithm/{self.version}")
        self.requires(f"boost-any/{self.version}")
        self.requires(f"boost-array/{self.version}")
        self.requires(f"boost-assert/{self.version}")
        self.requires(f"boost-concept-check/{self.version}")
        self.requires(f"boost-core/{self.version}")
        self.requires(f"boost-crc/{self.version}")
        self.requires(f"boost-function-types/{self.version}")
        self.requires(f"boost-iterator/{self.version}")
        self.requires(f"boost-lexical-cast/{self.version}")
        self.requires(f"boost-math/{self.version}")
        self.requires(f"boost-move/{self.version}")
        self.requires(f"boost-mpl/{self.version}")
        self.requires(f"boost-multiprecision/{self.version}")
        self.requires(f"boost-numeric-conversion/{self.version}")
        self.requires(f"boost-program-options/{self.version}")
        self.requires(f"boost-qvm/{self.version}")
        self.requires(f"boost-range/{self.version}")
        self.requires(f"boost-rational/{self.version}")
        self.requires(f"boost-static-assert/{self.version}")
        self.requires(f"boost-throw-exception/{self.version}")
        self.requires(f"boost-tokenizer/{self.version}")
        self.requires(f"boost-tuple/{self.version}")
        self.requires(f"boost-type-traits/{self.version}")
        self.requires(f"boost-utility/{self.version}")
        self.requires(f"boost-variant/{self.version}")
        self.requires(f"boost-container/{self.version}")
        self.requires(f"boost-serialization/{self.version}")
        self.requires(f"boost-fusion/{self.version}")
        self.requires(f"boost-integer/{self.version}")
        self.requires(f"boost-polygon/{self.version}")
        self.requires(f"boost-variant2/{self.version}")
        self.requires(f"boost-thread/{self.version}")
        self.requires(f"boost-endian/{self.version}")
        self.requires(f"boost-predef/{self.version}")

    def validate(self):
        check_min_cppstd(self, "14")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def build(self):
        pass

    def package(self):
        copy(self, "LICENSE_1_0.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, "*.hpp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.h", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.ipp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "boost_geometry")
        self.cpp_info.set_property("cmake_target_name", "Boost::geometry")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
