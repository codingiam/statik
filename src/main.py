import sys

from config import Config
from copystatic import copystatic
from utils import generate_pages_recursive

def main():
    if len(sys.argv) >= 2:
        Config.basepath = sys.argv[1]

    if len(sys.argv) >= 3:
        Config.dest = sys.argv[2]

    copystatic("static/", Config.dest)

    generate_pages_recursive("content/", "template.html", Config.dest)

if __name__ == "__main__":
    main()
