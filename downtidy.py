#!/usr/bin/env python3


from os import mkdir, scandir, remove
from os.path import expanduser, join, split, splitext, exists

from subprocess import PIPE, run
from sys import platform


# import tqdm # add progress bars ? maybe kinda useless if run frequently to tidy a small number of files
# import configparser,json # put config on an external file ?
# import argparse # for --folder option ?
from shutil import move
from hashlib import sha256
from datetime import datetime


__author__ = "xCoolHat"

__license__ = """MIT License

Copyright (c) 2021 xCoolHat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

sub_folders = {
    "Images": {
        "PNGs": ("png"),
        "JPGs": ("jpeg", "jpg", "jfif", "jp2"),
        "GIFs": ("gif", "gifv"),
        "WEBPs": ("avif", "webp", "heif"),
        "Vectors": ("svg", "eps"),
        "root": ("bmp", "tiff", "ico", "psd", "raw"),
    },
    "Videos": {
        "MP4s and WEBMs": ("mp4", "webm", "mpeg", "mpg", "m4v"),
        "MKVs": ("mkv"),
        "root": (
            "avi",
            "av1",
            "x264",
            "x265",
            "m2ts",
            "mov",
            "wmv",
            "flv",
            "3gp",
            "vob",
            "ogv",
            "hevc",
            "swf",
        ),
    },
    "Documents": {
        "Words": ("docx", "doc", "rtf", "odt", "docm"),
        "Spreadsheets": ("xlsx", "xls", "ods", "xlsb", "xlsm"),
        "Presentations": ("odp", "pps", "ppsx", "ppsm", "pptx", "ppt", "pptm"),
        "PDFs": ("pdf"),
        "Posters": ("odg", "pub"),
        "root": None,
    },
    "Archives": {
        "ISOs": ("iso", "vdi", "vhd", "squashfs", "bin"),
        "Packages(APKs and etc)": (
            "dmg",
            "apk",
            "crx",
            "xpi",
            "deb",
            "pkg",
            "apkg",
            "rpm",
        ),
        "ZIPs": ("zip"),
        "RARs": ("rar", "rar5"),
        "TARs": ("gz", "xz", "tar", "bz2", "zst"),
        "root": ("7z", "br", "lz", "lz4", "z", "pea"),
    },
    "Audio": {
        "Lossless": (
            "flac",
            "wav",
            "tta",
            "cue",
            "wma",
            "alac",
            "aiff",
            "tak",
            "ttk",
            "dff",
            "dsf",
            "ape",
        ),
        "Lossy": ("mp3", "m4a", "ogg", "aac", "m4b", "opus", "aax"),
        "MIDIs": ("mid", "midi"),
        "root": None,
    },
    "Executables": {
        "Java": ("jar", "class"),
        "EXEs": ("exe"),
        "MSIs": ("msi"),
        "AppImages": ("appimage"),
        "root": ("elf"),
    },
    "Scripts": {
        "CMD": ("cmd", "bat"),
        "PowerShell": ("ps1", "psm1", "psd1", "ps"),
        "Unix or Others": (
            "sh",
            "bash",
            "zsh",
            "command",
            "run",
            "ksh",
            "tmux",
            "fish",
            "csh",
            "tcsh",
        ),
        "root": None,
    },
    "Code Files": {
        "Web": (
            "js",
            "html",
            "mhtml",
            "htm",
            "ts",
            "jsx",
            "tsx",
            "css",
            "php",
            "xhtml",
            "vue",
            "rb",
        ),
        "Python": ("py", "ipynb"),
        "C C++ and C#": (
            "c",
            "h",
            "cpp",
            "hpp",
            "tcc",
            "tpp",
            "cxx",
            "hxx",
            "cc",
            "hh",
            "cs",
        ),
        "Build Tools": (
            "awk",
            "make",
            "makefile",
            "cmake",
            "cmake.in",
            "mk",
            "mkfile",
            "ninja",
            "ml",
            "gradle",
        ),
        "Lisp": ("el", "lisp", "cl", "lsp"),
        "Java": ("java", "kt"),
        "Rust": ("rs"),
        "Assembly": ("nasm", "asm"),
        "Objects or Config": (
            "dockerfile",
            "emacs",
            "nix",
            "xml",
            "json",
            "toml",
            "yaml",
            "yml",
        ),
        "Special Scripts": ("lua", "vbs", "ino", "ahk", "ahkl", "diff", "patch"),
        "Databases": ("sql", "db", "graphql"),
        "root": (
            "vb",
            "bf",
            "d",
            "hs",
            "hsc",
            "jl",
            "pas",
            "opencl",
            "r",
            "yacc",
            "perl",
            "go",
            "pl",
        ),
    },
    "Text Files": {
        "TXTs": ("txt"),
        "Markdown": ("md", "markdown", "rmd", "readme"),
        "CSVs": ("csv"),
        "Org-mode": ("org"),
        "LaTeX": ("latex", "tex"),
        "LOGs": ("log"),
        "Configs": ("ini", "conf", "cfg"),
        "Checksums and Signatures": (
            "sig",
            "asc",
            "md5",
            "sfv",
            "par",
            "par2",
            "md5sum",
            "sha1sum",
            "sha224sum",
            "sha256sum",
            "sha384sum",
            "sha512sum",
            "sha1",
            "sha224",
            "sha256",
            "sha384",
            "sha512",
        ),
        "root": ("rst", "rest", "strings", "man", "nfo"),
    },
    "Misc Stuff": {"root": ("torrent", "zsync")},
    "custom": None,
}

not_existent_folders, not_existent_subfolders = [], []

BUFFER_SIZE = 65536

files_to_tidy, files_not_tidied, dupe_files_deleted = 0, 0, 0


def check_for_win32_long_paths():
    from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE

    try:
        with OpenKey(
            HKEY_LOCAL_MACHINE, "SYSTEM\CurrentControlSet\Control\FileSystem"
        ) as key:
            return bool(QueryValueEx(key, "LongPathsEnabled")[0]), False
    except:
        print(
            "Error while checking if long paths are allowed! Assuming long paths are disallowed..."
        )
        return False, True


if platform == "win32" or platform == "cygwin":
    long_paths_enabled = check_for_win32_long_paths()
    if not long_paths_enabled[1] and not long_paths_enabled[0]:
        print(
            "Windows long paths are disabled in the Registry.\nIn the current version files who have a a destination path too long aren't moved"
        )


def top_folder_checks(downloads_folder):

    for folder in sub_folders.keys():
        folder_path = join(downloads_folder, folder)
        if not exists(folder_path) and folder != "root" and sub_folders[folder] != None:
            try:
                mkdir(join(downloads_folder, folder))
            except:
                print(f"Failure to create folder: {folder}")
                not_existent_folders.append(folder)


def sub_folder_checks(downloads_folder):

    for folder in sub_folders.keys():
        if (
            folder == "root"
            or folder in not_existent_folders
            and sub_folder[folder] != None
        ):
            continue
        search = list(sub_folders[folder].keys())
        search.remove("root")

        for sub_folder in search:
            sub_folder_fullpath = join(join(downloads_folder, folder), sub_folder)
            sub_folder_relative_path = join(folder, sub_folder)

            if not exists(sub_folder_fullpath):
                try:
                    mkdir(sub_folder_fullpath)
                except:
                    print(f"Failure to create (sub)folder: {sub_folder_relative_path}")
                    not_existent_subfolders.append(folder)


def get_new_paths(downloads_folder):

    global files_to_tidy
    to_tidy_preselection, to_tidy, new_paths = [], [], []

    with scandir(downloads_folder) as it:
        for entry in it:
            if entry.is_file():
                to_tidy_preselection.append(entry.name)

    for file_name in to_tidy_preselection:

        loop_exit = False
        ext = splitext(file_name)[1][1:].lower()

        for top_folder in sub_folders.items():
            if top_folder[1] != None:
                for sub_folder in top_folder[1].items():
                    if (
                        sub_folder[1] != None
                        and ext in sub_folder[1]
                        and sub_folder[0] != "root"
                    ):
                        new_paths.append(
                            join(
                                join(
                                    join(downloads_folder, top_folder[0]), sub_folder[0]
                                ),
                                file_name,
                            )
                        )
                        to_tidy.append(join(downloads_folder, file_name))
                        loop_exit = True
                        break
                    elif (
                        sub_folder[1] != None
                        and ext in sub_folder[1]
                        and sub_folder[0] == "root"
                    ):
                        new_paths.append(
                            join(join(downloads_folder, top_folder[0]), file_name)
                        )
                        to_tidy.append(join(downloads_folder, file_name))
                        loop_exit = True
                        break
                if loop_exit:
                    break

    files_to_tidy = len(to_tidy)

    print(f"{files_to_tidy} files to tidy.")

    return to_tidy, new_paths


def tidy_files(to_tidy: tuple):
    global files_not_tidied
    global dupe_files_deleted
    for j in range(len(to_tidy[0])):

        if not exists(to_tidy[1][j]) and (
            (platform != "win32" and platform != "cygwin")
            or ((platform == "win32" or platform == "cygwin") and long_paths_enabled)
        ):
            try:
                move(src=to_tidy[0][j], dst=to_tidy[1][j])
            except:
                print(f"Error moving file: {split(to_tidy[0][j])[1]}")
                files_not_tidied += 1

        elif (platform == "win32" or platform == "cygwin") and not long_paths_enabled:
            if (
                len(to_tidy[1][j]) >= 259
            ):  # TODO: files that get a path too long on win32 aren't moved think of a better way to handle, or just leave it as it is
                print(f"Skipped moving file: {split(to_tidy[0][j])[1]}")
                files_not_tidied += 1
                continue
            else:
                try:
                    move(src=to_tidy[0][j], dst=to_tidy[1][j])
                except:
                    print(f"Error moving file {split(to_tidy[0][j])[1]}")
                    files_not_tidied += 1

        elif exists(to_tidy[1][j]):

            if compare_file_hashes(to_tidy[0][j], to_tidy[1][j]):
                print(f"Duplicate file found, removed: {split(to_tidy[0][j])[1]}")
                try:
                    remove(to_tidy[0][j])
                    dupe_files_deleted += 1
                except:
                    print(f"Error removing file: {split(to_tidy[0][j])[1]}")

                    files_not_tidied += 1
            else:

                print(
                    f"Filename collision found: {split(to_tidy[0][j])[1]} appended current date to filename"
                )
                try:
                    destination = splitext(to_tidy[1][j])
                    move(
                        to_tidy[0][j],
                        destination[0]
                        + datetime.now().strftime("%d-%m-%Y %H-%M-%S")
                        + destination[1],
                    )
                except:
                    print(f"Error moving file {split(to_tidy[0][j])[1]}")
                    files_not_tidied += 1
        else:
            print(
                "Some case I didn remember FIXME!!!!\
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            )
            files_not_tidied += 1


def compare_file_hashes(path_src, path_dst):

    src, dst = sha256(), sha256()

    with open(path_src, "rb") as f, open(path_dst, "rb") as f2:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            src.update(data)
        while True:
            data = f2.read(BUFFER_SIZE)
            if not data:
                break
            dst.update(data)

    return src.hexdigest() == dst.hexdigest()


def main():

    if platform == "win32" or platform == "cygwin":
        # reference: "adapted" from here https://stackoverflow.com/a/35851955 uses ctypes winapis
        from ctypes import (
            windll,
            wintypes,
            Structure,
            POINTER,
            c_wchar_p,
            byref,
            WinError,
        )
        from uuid import UUID

        # ctypes GUID copied from MSDN sample code
        class GUID(Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8),
            ]

            def __init__(self, uuidstr):
                uuid = UUID(uuidstr)
                Structure.__init__(self)
                (
                    self.Data1,
                    self.Data2,
                    self.Data3,
                    self.Data4[0],
                    self.Data4[1],
                    rest,
                ) = uuid.fields
                for i in range(2, 8):
                    self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xFF

        SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            POINTER(GUID),
            wintypes.DWORD,
            wintypes.HANDLE,
            POINTER(c_wchar_p),
        ]

        def _get_known_folder_path(uuidstr):
            pathptr = c_wchar_p()
            guid = GUID(uuidstr)
            if SHGetKnownFolderPath(byref(guid), 0, 0, byref(pathptr)):
                raise WinError()
            return pathptr.value

        # Downloads folder GUID
        FOLDERID_Downloads = "{374DE290-123F-4565-9164-39C4925E467B}"

        def get_downloads_folder():
            return _get_known_folder_path(FOLDERID_Downloads)

    elif platform == "darwin" or platform == "linux":

        def get_downloads_folder():
            home = expanduser("~")
            if not home:
                raise ValueError("$HOME environment variable not set or unknown")

            user_config_path = join(join(home, ".config"), "user-dirs.dirs")
            if exists(user_config_path):

                if platform == "linux":
                    try:
                        check_config = run(["xdg-user-dir", "DOWNLOAD"], stdout=PIPE)
                        downloads_path = str(check_config.stdout.decode("utf-8"))

                        if downloads_path != home and downloads_path != "":
                            if not exists(downloads_path):
                                mkdir(downloads_path)
                            return downloads_path

                    except FileNotFoundError:
                        print(
                            "Warning:Package xdg-user-dirs not installed or not found in $PATH"
                        )
                        print("Checking for config file...")
                        with open(user_config_path, "r") as config_file:
                            for line in config_file:
                                if "XDG_DOWNLOAD_DIR=" in line:
                                    to_parse = line[17:-1].strip('"')
                                    if "$HOME" in to_parse:
                                        return to_parse.replace("$HOME", home)
            else:
                downloads_path = join(home, "Downloads")
                if exists(downloads_path):
                    return downloads_path
                else:
                    print(
                        "Didn't found a standard/configured Downloads folder. Trying to create one..."
                    )
                    try:
                        mkdir(downloads_path)
                        print("Created a Downloads folder at your user home directory")
                    except:
                        raise ValueError(
                            "Failed to create create a downloads folder.\nExiting downtidy..."
                        )

    else:
        raise OSError("At the moment this OS isn't supported. Sorry!")

    tidy_files(get_new_paths(get_downloads_folder()))

    print(f"Files tidied: {files_to_tidy - files_not_tidied - dupe_files_deleted}")
    print(f"Duplicate files removed: {dupe_files_deleted}")
    print(f"Files not tidied: {files_not_tidied}")
    print("All Done!")


if __name__ == "__main__":
    main()
    exit(0)
