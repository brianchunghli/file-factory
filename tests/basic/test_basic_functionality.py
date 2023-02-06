#!/usr/bin/env python3


def test_run_help(test_program, pytester):
    data = pytester.run(test_program, '-h')
    assert data is not None


def test_run_debug(test_program, pytester):
    data = pytester.run(test_program, '-d')
    assert data is not None


def test_create_files_cpp(test_program, pytester):
    data = pytester.run(test_program, 'cpp', 'test')
    data.stdout.fnmatch_lines("test.cpp created.\n")


def test_create_files_cpp_with_main_args(test_program, pytester):
    data = pytester.run(test_program, 'cpp', '-m', 'test')
    data.stdout.fnmatch_lines("test.cpp created.\n")
    data = pytester.run('cat', 'test.cpp')
    data.stdout.fnmatch_lines("int main(const int argc, const char* argv[]) {")


def test_create_files_c(test_program, pytester):
    data = pytester.run(test_program, 'c', 'test')
    data.stdout.fnmatch_lines("test.c created.\n")


def test_create_files_c_with_main_args(test_program, pytester):
    data = pytester.run(test_program, 'c', '-m', 'test')
    data.stdout.fnmatch_lines("test.c created.\n")
    data = pytester.run('cat', 'test.c')
    data.stdout.fnmatch_lines("int main(int argc, char* argv[]) {")


def test_create_files_sh(test_program, pytester):
    data = pytester.run(test_program, 'sh', 'test')
    data.stdout.fnmatch_lines("test.sh created.\n")


def test_create_files_zsh(test_program, pytester):
    data = pytester.run(test_program, 'zsh', 'test')
    data.stdout.fnmatch_lines("test.zsh created.\n")


def test_create_files_py(test_program, pytester):
    data = pytester.run(test_program, 'py', 'test')
    data.stdout.fnmatch_lines("test.py created.\n")


def test_create_files_make(test_program, pytester):
    pytester.run(test_program, 'c', 'test')
    data = pytester.run(test_program, 'make', 'test.c')
    data.stdout.fnmatch_lines("Makefile created.\n")


def test_create_files_cmake(test_program, pytester):
    import os
    pytester.run(test_program, 'c', 'test')
    data = pytester.run(test_program, 'cmake', 'test.c')
    build_exists = os.path.exists('build/')
    assert build_exists
