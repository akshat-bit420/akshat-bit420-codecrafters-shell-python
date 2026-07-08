import os
import sys
import subprocess

VALID_COMMANDS = set({"exit", "echo", "type"})


def find_executable(command: str) -> str | None:
    path_env = os.environ.get("PATH")
    if not path_env:
        return None

    for directory in path_env.split(os.pathsep):
        candidate = os.path.join(directory, command)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate

    return None


def main() -> None:
    while True:
        sys.stdout.write("$ ")
        line = input()

        if not line.strip():
            continue

        parts = line.split()
        cmd = parts[0]

        if cmd == "exit":
            sys.exit(0)

        elif cmd == "echo":
            print(" ".join(parts[1:]))

        elif cmd == "type":
            if len(parts) < 2:
                continue

            target = parts[1]
            if target in VALID_COMMANDS:
                print(f"{target} is a shell builtin")
            else:
                found = find_executable(target)
                if found:
                    print(f"{target} is {found}")
                else:
                    print(f"{target}: not found")

        else:
            found = find_executable(cmd)
            if not found:
                print(f"{line}: command not found")
            else:
                res = subprocess.run(args=parts)
                sys.exit(res.returncode)
    else:
        res = subprocess.run(args=parts)


if __name__ == "__main__":
    main()