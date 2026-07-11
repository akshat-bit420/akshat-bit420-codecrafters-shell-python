import os
import sys
import shutil
import subprocess
from subprocess import run

def main():
     built_in_commands = ["echo", "exit", "type", "pwd", "cd"]
     while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        parts = command.split()
        prog = parts[0]
        if command == "pwd":
             print(os.getcwd())
             continue
        if command == "exit":
             break
        elif command.startswith("echo "):
             print(command[5:])
             
        elif command.startswith("cd ") or command == "cd":
                if len(parts) > 1:
                    target_path = parts[1]
                    if target_path == "~":
                        target_path = os.getenv("HOME")
                else:
                    target_path = os.getenv("HOME")
                try:
                    os.chdir(target_path)
                except (FileNotFoundError, TypeError):
                    print(f"cd: {target_path}: No such file or directory") 
                except Exception:
                    print(f"cd: {target_path}: No such file or directory")
                continue                      
        elif command.startswith("type "):
             subject = command[5:]
             if subject in ["echo", "exit", "type", "pwd", "cd"]:
                 print(f"{subject} is a shell builtin")
             elif path := shutil.which(subject):
                 print(f"{subject} is {path}")
             else:
                print(f"{subject}: not found")
        else:
            parts = command.split()
            if not parts:
                continue
            cmd = parts[0]
            path = shutil.which(cmd)
            if not path:
                print(f"{cmd}: command not found")
            else:
                sys.stdout.flush()
                subprocess.run(parts, executable=path)
                sys.stdout.flush()

if __name__ == "__main__":
     main()

