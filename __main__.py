
from core.args import get_arguments
if __name__ == '__main__':
    arguments = get_arguments()
    if "TUI" == arguments.mode:
        print("starting FTP server in TUI mode.")
    if "GUI" == arguments.mode:
        print("starting FTP server in GUI mode.")
