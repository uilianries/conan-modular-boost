from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=2.4"


class BoostAccumulatorsConan(ConanFile):
    name = "boost-accumulators"
    description = "Framework for incremental calculation, and collection of statistical accumulators"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "error-handling", "header-only")
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
        self.requires(f"boost-array/{self.version}")
        self.requires(f"boost-assert/{self.version}")
        self.requires(f"boost-circular-buffer/{self.version}")
        self.requires(f"boost-concept-check/{self.version}")
        self.requires(f"boost-core/{self.version}")
        self.requires(f"boost-fusion/{self.version}")
        self.requires(f"boost-iterator/{self.version}")
        self.requires(f"boost-mpl/{self.version}")
        self.requires(f"boost-numeric-conversion/{self.version}")
        self.requires(f"boost-ublas/{self.version}")
        self.requires(f"boost-parameter/{self.version}")
        self.requires(f"boost-preprocessor/{self.version}")
        self.requires(f"boost-range/{self.version}")
        self.requires(f"boost-serialization/{self.version}")
        self.requires(f"boost-static-assert/{self.version}")
        self.requires(f"boost-throw-exception/{self.version}")
        self.requires(f"boost-tuple/{self.version}")
        self.requires(f"boost-type-traits/{self.version}")
        self.requires(f"boost-typeof/{self.version}")

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
        self.cpp_info.set_property("cmake_file_name", "boost_accumulators")
        self.cpp_info.set_property("cmake_target_name", "Boost::accumulators")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
