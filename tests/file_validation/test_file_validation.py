#!/usr/bin/env python3


def test_makefile_contents(test_program, pytester):
    pytester.run(test_program, 'c', 'test')
    pytester.run(test_program, 'make', '-f -Wall -Werror', 'test.c')
    data = pytester.run('cat', 'Makefile').stdout
    data.re_match_lines('CFLAGS = -Wall -Werror -fsanitize=address -std=c99')


def test_cmakefile_contents(test_program, pytester):
    pytester.run(test_program, 'c', 'test')
    pytester.run(test_program, 'cmake', 'test.c')
    data = pytester.run('cat', 'CMakeLists.txt').stdout
    data.re_match_lines('project(test)')
    data.re_match_lines('cmake_minimum_required(VERSION 3.18.4)')
    data.re_match_lines('set(CMAKE_CXX_STANDARD 99)')
