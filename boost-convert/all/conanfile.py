from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostConvertConan(ConanFile):
    name = "boost-convert"
    description = "An extendible and configurable type-conversion framework"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "miscellaneous", "string", "header-only")
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
        self.requires(f"boost-core/{self.version}")
        self.requires(f"boost-function-types/{self.version}")
        self.requires(f"boost-lexical-cast/{self.version}")
        self.requires(f"boost-math/{self.version}")
        self.requires(f"boost-mpl/{self.version}")
        self.requires(f"boost-optional/{self.version}")
        self.requires(f"boost-parameter/{self.version}")
        self.requires(f"boost-range/{self.version}")
        self.requires(f"boost-spirit/{self.version}")
        self.requires(f"boost-type-traits/{self.version}")

    def validate(self):
        check_min_cppstd(self, "11")

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
        self.cpp_info.set_property("cmake_file_name", "boost_convert")
        self.cpp_info.set_property("cmake_target_name", "Boost::convert")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
