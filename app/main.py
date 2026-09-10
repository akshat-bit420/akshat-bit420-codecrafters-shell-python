# me trying to build my own shell, I like to suffer

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

    i = 0

    while i < len(cmd_string):

        char = cmd_string[i]

        # Backslash outside quotes
        if char == "\\" and not in_single_quote and not in_double_quote:
            if i + 1 < len(cmd_string):
                current_args += cmd_string[i + 1]
                i += 2
                continue

        # Backslash inside double quotes
        elif char == "\\" and in_double_quote:
            if i + 1 < len(cmd_string):
                next_char = cmd_string[i + 1]

                # Inside double quotes, only \ and " are escaped
                if next_char == "\\" or next_char == '"':
                    current_args += next_char
                    i += 2
                    continue

                # Otherwise, keep the backslash literally
                current_args += char
                i += 1
                continue

        # Single quote
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote

        # Double quote
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote

        # Space outside quotes
        elif char == " " and not in_single_quote and not in_double_quote:
            if current_args:
                args.append(current_args)
                current_args = ""

        else:
            current_args += char

        i += 1

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

        # Handle output redirection
        output_file = None

        if ">" in parts:
            redirect_index = parts.index(">")
            output_file = parts[redirect_index + 1]
            parts = parts[:redirect_index]

        elif "1>" in parts:
            redirect_index = parts.index("1>")
            output_file = parts[redirect_index + 1]
            parts = parts[:redirect_index]

        if not parts:
            continue

        prog = parts[0]

        if output_file:
            output = open(output_file, "w")
        else:
            output = sys.stdout

        # 1. pwd
        if prog == "pwd":
            print(os.getcwd(), file=output)
            if output_file:
                output.close()
            continue

        # 2. exit
        elif prog == "exit":
            if output_file:
                output.close()
            break

        # 3. echo
        elif prog == "echo":
            print(' '.join(parts[1:]), file=output)
            if output_file:
                output.close()
            continue

        # 4. cd
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

            if output_file:
                output.close()

            continue

        # 5. type
        elif prog == "type":
            if len(parts) > 1:
                subject = parts[1]

                if subject in ["echo", "exit", "type", "pwd", "cd"]:
                    print(f"{subject} is a shell builtin", file=output)

                elif path := shutil.which(subject):
                    print(f"{subject} is {path}", file=output)

                else:
                    print(f"{subject}: not found", file=output)

            if output_file:
                output.close()

            continue

        # External commands
        else:
            path = shutil.which(prog)

            if not path:
                print(f"{prog}: command not found")

            else:
                sys.stdout.flush()

                if output_file:
                    subprocess.run(
                        parts,
                        executable=path,
                        stdout=output
                    )
                else:
                    subprocess.run(
                        parts,
                        executable=path
                    )

                sys.stdout.flush()

        if output_file:
            output.close()

if __name__ == "__main__":
     main()