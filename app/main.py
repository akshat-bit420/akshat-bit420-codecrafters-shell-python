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

        output_file = None
        error_file = None

        output_mode = "w"

        # Output redirection
        if ">>" in parts:
            redirect_index = parts.index(">>")
            output_file = parts[redirect_index + 1]
            output_mode = "a"
            parts = parts[:redirect_index]

        elif "1>>" in parts:
            redirect_index = parts.index("1>>")
            output_file = parts[redirect_index + 1]
            output_mode = "a"
            parts = parts[:redirect_index]

        elif ">" in parts:
            redirect_index = parts.index(">")
            output_file = parts[redirect_index + 1]
            output_mode = "w"
            parts = parts[:redirect_index]

        elif "1>" in parts:
            redirect_index = parts.index("1>")
            output_file = parts[redirect_index + 1]
            output_mode = "w"
            parts = parts[:redirect_index]

        # Error redirection
        if "2>" in parts:
            redirect_index = parts.index("2>")
            error_file = parts[redirect_index + 1]
            parts = parts[:redirect_index]

        if not parts:
            continue

        prog = parts[0]

        # Decide stdout
        if output_file:
            output = open(output_file, output_mode)
        else:
            output = sys.stdout

        # Decide stderr
        if error_file:
            error_output = open(error_file, "w")
        else:
            error_output = sys.stderr

        # -------------------------
        # pwd
        # -------------------------
        if prog == "pwd":

            print(os.getcwd(), file=output)

        # -------------------------
        # exit
        # -------------------------
        elif prog == "exit":

            if output_file:
                output.close()

            if error_file:
                error_output.close()

            break

        # -------------------------
        # echo
        # -------------------------
        elif prog == "echo":

            print(" ".join(parts[1:]), file=output)

        # -------------------------
        # cd
        # -------------------------
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
                print(
                    f"cd: {target_path}: No such file or directory",
                    file=error_output
                )

            except Exception:
                print(
                    f"cd: {target_path}: No such file or directory",
                    file=error_output
                )

        # -------------------------
        # type
        # -------------------------
        elif prog == "type":

            if len(parts) > 1:

                subject = parts[1]

                if subject in built_in_commands:

                    print(
                        f"{subject} is a shell builtin",
                        file=output
                    )

                elif path := shutil.which(subject):

                    print(
                        f"{subject} is {path}",
                        file=output
                    )

                else:

                    print(
                        f"{subject}: not found",
                        file=error_output
                    )

        # -------------------------
        # External command
        # -------------------------
        else:

            path = shutil.which(prog)

            if not path:

                print(
                    f"{prog}: command not found",
                    file=error_output
                )

            else:

                sys.stdout.flush()

                subprocess.run(
                    parts,
                    executable=path,
                    stdout=output,
                    stderr=error_output
                )

                sys.stdout.flush()

        # -------------------------
        # Close redirected files
        # -------------------------
        if output_file:
            output.close()

        if error_file:
            error_output.close()


if __name__ == "__main__":
     main()