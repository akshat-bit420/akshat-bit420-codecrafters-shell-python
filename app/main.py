import sys
import shutil
import subprocess

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            subject = command[5:]
            if subject in ["echo", "exit", "type"]:
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