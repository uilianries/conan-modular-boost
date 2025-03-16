from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=2.1"


class BoostHeadersConan(ConanFile):
    name = "boost-headers"
    description = "This is a fake library that installs the Boost headers"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def build(self):
        pass

    def package(self):
        copy(self, "LICENSE_1_0.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, ".gitkeep", os.path.join(self.source_folder, "include", "boost", "headers"),
             os.path.join(self.package_folder, "include", "boost", "headers"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "boost_headers")
        self.cpp_info.set_property("cmake_target_name", "Boost::headers")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
