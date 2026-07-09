# import sys
# import shutil
# import subprocess
# from subprocess import run

# def main():
#     built_in_commands = ["echo", "exit", "type", "pwd"]
#     while True:
#         sys.stdout.write("$ ")
#         sys.stdout.flush()
#         command = input()
#         if command == pwd:
#             print(os.getcwd())
#             continue
#         if command == "exit":
#             break
#         elif command.startswith("echo "):
#             print(command[5:])
#         elif command.startswith("type "):
#             subject = command[5:]
#             if subject in ["echo", "exit", "type"]:
#                 print(f"{subject} is a shell builtin")
#             elif path := shutil.which(subject):
#                 print(f"{subject} is {path}")
#             else:
#                 print(f"{subject}: not found")
#         else:
#             parts = command.split()
#             if not parts:
#                 continue
#             cmd = parts[0]
#             path = shutil.which(cmd)
#             if not path:
#                 print(f"{cmd}: command not found")
#             else:
#                 sys.stdout.flush()
#                 subprocess.run(parts, executable=path)
#                 sys.stdout.flush()

# if __name__ == "__main__":
#     main()



import os
import shutil
import sys
import subprocess
from subprocess import run


def main():
    built_in_commands = ["echo", "exit", "type", "pwd"]
    while True:
        sys.stdout.write("$ ")
        pass

        # get user's input
        command = input()
        prog = command.split()[0]
        if command == "pwd":
            print(os.getcwd())
            continue
        if command == "exit":
            break
        elif command.startswith("echo "):
            print(command[5:])
            continue
        elif command.startswith("type "):
            cmd = command[5:]
            if cmd in built_in_commands:
                print(f"{cmd} is a shell builtin")
            elif path := shutil.which(cmd):
                print(f"{cmd} is {path}")
            else:
                print(f"{cmd} not found")
            continue
        elif shutil.which(prog):
            subprocess.run(command.split())
            continue
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()