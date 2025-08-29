import argparse

parser = argparse.ArgumentParser(prog="FTP-server",
                                 description="Simple FTP-server with 2 modes: GUI and TUI")

parser.add_argument("-m","--mode",type=str,default="GUI",choices=("GUI","TUI"))

def get_arguments():
    return parser.parse_args()
