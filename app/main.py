import sys
import shutil

def main():
    while True:
        sys.stdout.write("$ ")
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
            print(f"{command}: command not found")



if __name__ == "__main__":
    main()
