require "formula"

class Hi < Formula
    desc "A command line tool for saying hello"
    homepage "https://github.com/wcarhart/hi"
    url "https://github.com/wcarhart/hi/archive/v1.0.tar.gz"
    sha256 "ec1f1fc76e228ec3853c95d7c1e46d68ee2b33335c855db65f80f7c208d880c2"

    depends_on "bash"

    def install
        bin.install "hi"
    end
end
