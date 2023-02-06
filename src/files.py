#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import textwrap
from typing import Dict, Tuple, Union

COLORS: dict = {
    'r': '[38;5;1m',
    'g': '[38;5;2m',
    'y': '[38;5;11m',
}


def color_print(msg: str, color='g', **kwargs) -> None:
    '''
    Color print a message.
    '''
    start = COLORS.get(color, '[0;0m')
    print(f'\033{start}{msg}\033[0;0m', **kwargs)


def prog_print(msg: str, **kwargs) -> None:
    '''
    Program print a message
    '''
    print(f'{os.path.basename(sys.argv[0])}: {msg}', **kwargs)


'''
Basic file factory for c/c++, python, shell, 
make and cmake files.
'''


def parseArguments() -> Dict[str, Union[list[str], str, bool]]:
    '''
    Parses command line arguments
    '''

    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        exit_on_error=True,
        description="Basic file factory.",
    )
    subp = parser.add_subparsers(dest='file_type',
                                 title='subcommands',
                                 required=True)

    main_flags = argparse.ArgumentParser(add_help=False)
    main_flags.add_argument('file_name',
                            nargs='+',
                            help='<program file>, list <dependencies...>')
    main_flags.add_argument('-d',
                            '--debug',
                            action='store_true',
                            help='print debugging related information')
    # python files
    py = subp.add_parser('py',
                         parents=[main_flags],
                         help='file generator for py files')

    # make/cmake files
    make_flags = argparse.ArgumentParser(add_help=False)
    make_flags.add_argument('-std',
                            '--standard',
                            nargs=1,
                            type=int,
                            metavar='<std>',
                            help='set standard for compilation')
    make_flags.add_argument('-f',
                            '--flags',
                            nargs=1,
                            type=str,
                            help='replaces compiler flags')
    make = subp.add_parser('make',
                           parents=[main_flags, make_flags],
                           help='file generator for cmake files')
    cmake = subp.add_parser('cmake',
                            parents=[main_flags, make_flags],
                            help='file generator for make files')

    # c/cpp files
    c_flags = argparse.ArgumentParser(add_help=False)
    c_flags.add_argument('-m',
                         '--main',
                         action='store_true',
                         help='include argc and argv in main')
    c = subp.add_parser('c',
                        parents=[main_flags, c_flags],
                        help='file generator for c files')
    cpp = subp.add_parser('cpp',
                          parents=[
                              main_flags,
                              c_flags,
                          ],
                          help='file generator for cpp files')
    cpp.add_argument('-cp',
                     '--competitive',
                     action='store_true',
                     help='competitive programming template')

    # zsh/shell files
    sh = subp.add_parser('sh',
                         parents=[main_flags],
                         help='file generator for sh files')
    zsh = subp.add_parser('zsh',
                          parents=[main_flags],
                          help='file generator for zsh files')

    return vars(parser.parse_args())


def gen_makefile_and_cmakefile(args: dict) -> str:

    filename, suffix = args['file_name'][0].split('.')
    cflags = ' -Wall -Weffc++ -Wextra -Wsign-conversion --pedantic-errors'

    if args['flags']:
        cflags = ' '.join(args['flags'])
    std = '20'
    dep_files = ''
    if suffix == 'c':
        std = '99'
    if args['file_name'][1:]:
        dep_files = ' ' + ' '.join(
            (f'{f}.{suffix}' if len(f.split('.')) == 1 else f
             for f in args['file_name'][1:]))
    if args['file_type'] == 'cmake':
        if not os.path.exists(os.getcwd() + 'r/build'):
            subprocess.run(['mkdir', 'build'], capture_output=True)
        # CMakeLists file details
        file_contents = textwrap.dedent(f"""\
        # options
        cmake_minimum_required(VERSION 3.18.4)
        project({filename})
        set(CMAKE_CXX_STANDARD {std})
        set(CMAKE_EXPORT_COMPILE_COMMANDS ON)\n
        add_compile_options({cflags})
        add_executable({filename} {filename}.{suffix}{dep_files})
        """)
    else:
        # based on
        # https://stackoverflow.com/questions/1950926/create-directories-using-make-file
        std = 'c++20'
        compiler = 'g++'
        if suffix == 'c':
            compiler = 'gcc'
            std = 'c99'
        cflags = cflags + ' -fsanitize=address'  # issues with cmake and fsanitize
        compile_command = r'${CC} ${CFLAGS}'
        file_contents = textwrap.dedent(f"""\
        CC = {compiler} 
        CFLAGS ={cflags} -std={std}
        MKDIR_P := mkdir -p
        OUT_DIR := build

        .PHONY: noargs {filename} clean

        noargs:
        \t@echo 'make <{filename} | clean>'
        clean:
        \trm -rf $(OUT_DIR)
        {filename}: $(OUT_DIR)/{filename}

        $(OUT_DIR):
        \t$(MKDIR_P) $(OUT_DIR)
        $(OUT_DIR)/{filename}: {filename}.{suffix}{dep_files} | $(OUT_DIR) 
        \t{compile_command} -o $(OUT_DIR)/{filename} {filename}.{suffix}{dep_files}
        """)
    return file_contents


def generate_file(args: dict) -> str:
    """
    Generates the file contents for the
    file.
    """
    contents: str = ''
    success, message = check_args(args)
    if not success:
        prog_print(message)
        return contents
    filetype = args['file_type']
    if filetype in ["c", "cpp"]:
        main = 'int main() {\n\n  return 0;\n}'
        header = '#include <stdio.h>\n#include <stdlib.h>\n\n'
        if args['main']:
            main = 'int main(int argc, char* argv[]) {\n\n  return 0;\n}'
        if filetype == 'cpp':
            header = '#include <iostream>\n\n'
            if args['main']:
                main = main.replace('int argc', 'const int argc').replace(
                    'char* argv[]', 'const char* argv[]')
            if args['competitive']:
                header = textwrap.dedent('''\
                #include <iostream>

                void solve() {}

                ''')
                main = main.replace(
                    '\n\n  return 0;',
                    textwrap.dedent('''
                \tstd::string tc;
                \tstd::cin >> tc;
                \tfor (auto t = 0; t < std::stoi(tc); ++t) {
                    // cout << "Case #" << t << ": ";
                    solve();
                \t}
                \treturn 0;
                '''))
        contents = header + main
    elif filetype == "py":
        contents = textwrap.dedent("""\
        #!/usr/bin/env python3\n\n
        def main() -> None:
            pass\n\n
        if __name__ == '__main__':
            main()
        """)
    elif filetype in ["sh", "zsh"]:
        contents = f"#!/bin/{filetype}\n"
    elif filetype in ["cmake", "make"]:
        contents = gen_makefile_and_cmakefile(args)
    return contents


def check_args(args: dict) -> Tuple[bool, str]:
    '''
    Check validity of arguments
    '''
    success = True
    err_message = ''
    filetype, filename = args['file_type'], args['file_name'][0]
    has_suffix = filename.split('.')
    if len(has_suffix) == 2 and filetype not in ('cmake', 'make'):
        err_message = f'extraneous suffix \'{has_suffix[1]}\''
        success = False
    elif filetype == 'cmake' or filetype == 'make':
        suffix = filename.split('.')
        if len(suffix) != 2:
            success = False
            err_message = f'invalid file \'{filename}\''
        elif suffix[1] != 'cpp' and suffix[1] != 'c':
            success = False
            err_message = f'invalid file \'{filename}\''
        if not os.path.exists(os.getcwd() + f'/{filename}') and success:
            success = False
            err_message = f'\'{filename}\' cannot be found in current directory'
    return success, err_message


def main() -> None:
    opts = parseArguments()
    if opts['debug']:
        color_print('Provided arguments:')
        for arg in opts:
            print(f'{arg}:', opts[arg])
    file_contents = generate_file(opts)
    new_file, suffix = opts['file_name'][0], opts['file_type']
    if not file_contents:
        return
    filename = f"{new_file}.{suffix}"
    if os.path.exists(os.path.abspath(filename)):
        message = f'File exists. Replace {os.path.basename(filename)}? '
        if input(message) not in ('yes', 'y', 'Yes'):
            print("file creation aborted")
            return
    if suffix == 'cmake':
        filename = 'CMakeLists.txt'
    if suffix == 'make':
        filename = 'Makefile'
    with open(filename, "w") as w:
        w.write(file_contents)
    if suffix in ["zsh", "sh", "py"]:
        subprocess.run(["chmod", "+x", filename])
    if suffix == 'cmake':
        subprocess.run(['cmake', '-S', '.', '-B', 'build/'])
    print(f"{filename} created.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        prog_print('\nkeyboard interrupted.')
