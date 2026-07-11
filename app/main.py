import os
import sys
import shutil
import subprocess
from subprocess import run

def parse_argument(cmd_string):
    args = []
    current_args = ""
    in_single_quote = False
    in_double_quote = False

    for char in cmd_string:
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif char == " " and not in_single_quote and not in_double_quote:       
            if current_args:
                args.append(current_args)
                current_args = ""
        else:
            current_args += char

    if current_args:
        args.append(current_args)

    return args


def main():
     built_in_commands = ["echo", "exit", "type", "pwd", "cd"]
     while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        parts = parse_argument(command)
        if not parts:
            continue
        prog = parts[0]
        
        # 1. Switched to 'prog == "pwd"'
        if prog == "pwd":
             print(os.getcwd())
             continue
             
        # 2. Switched to 'prog == "exit"'
        elif prog == "exit":
             break
             
        elif prog == "echo":
            # 3. Fixed '' to ' ' to preserve space between separate words
            print(' '.join(parts[1:]))
             
        # 4. Switched to 'prog == "cd"'
        elif prog == "cd":
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
                
        elif prog == "type":
            if len(parts) > 1:
                subject = parts[1]
                if subject in ["echo", "exit", "type", "pwd", "cd"]:
                    print(f"{subject} is a shell builtin")
                elif path := shutil.which(subject):
                    print(f"{subject} is {path}")
                else:
                    print(f"{subject}: not found")
        else:
            path = shutil.which(prog)
            if not path:
                print(f"{prog}: command not found")
            else:
                sys.stdout.flush()
                subprocess.run(parts, executable=path)
                sys.stdout.flush()

if __name__ == "__main__":
     main()