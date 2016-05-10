from conans import ConanFile, CMake, tools
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "memsharded")

class VSModulesTestConan(ConanFile):
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    requires = "MyMath/0.1@%s/%s" % (username, channel)

    def build(self):
        param = "x86" if self.settings.arch == "x86" else "amd64"
        vcvars = 'call "%%vs140comntools%%../../VC/vcvarsall.bat" %s' % param
        lib_path = self.deps_cpp_info.lib_paths[0]
        libs = " ".join("%s/%s" % (lib_path, lib) for lib in self.deps_cpp_info.libs)
        command = ('%s && cl /EHsc /experimental:module /module:reference %s %s/main.cpp '
                     % (vcvars, libs, self.conanfile_directory, ))
        self.run(command)
        
    def test(self):
        self.run("main")
