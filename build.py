import os
import shutil

import PyInstaller.__main__


def main():
    build_dir = "build"
    dist_dir = "dist"

    shutil.rmtree(build_dir, ignore_errors=True)
    shutil.rmtree(dist_dir, ignore_errors=True)

    os.makedirs(dist_dir, exist_ok=True)
    args = ["--onefile", "--clean"]
    args += ["-n", "overlay_timer", "-i", "icon.ico"]
    args += ["--optimize", "2", "-w", "main.py"]
    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    main()
