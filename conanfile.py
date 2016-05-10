from conans import ConanFile, CMake, tools
import os


class VSModulesConan(ConanFile):
    name = "MyMath"
    version = "0.1"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    exports = "mymath.ixx"

    def build(self):
        param = "x86" if self.settings.arch == "x86" else "amd64"
        # Missing handling of build_type, but lets keep it simple
        vcvars = 'call "%%vs140comntools%%../../VC/vcvarsall.bat" %s' % param
        self.run('%s && cl /c /experimental:module mymath.ixx' % vcvars)
        self.run('%s && lib mymath.obj -OUT:mymath.lib' % vcvars)

    def package(self):
        self.copy("*.lib", "lib") 
        self.copy("*.ifc", "lib") 

    def package_info(self):
        self.cpp_info.libs = ["MyMath.ifc", "mymath.lib"]
