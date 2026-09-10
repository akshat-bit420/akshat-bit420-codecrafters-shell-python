# me trying to build my own shell, I like to suffer

import os
import sys
import shutil
import subprocess


def parse_argument(cmd_string):

    args = []
    current_args = ""

    in_single_quote = False
    in_double_quote = False

    i = 0

    while i < len(cmd_string):

        char = cmd_string[i]

        if char == "\\" and not in_single_quote and not in_double_quote:
            if i + 1 < len(cmd_string):
                current_args += cmd_string[i + 1]
                i += 2
                continue

        elif char == "\\" and in_double_quote:
            if i + 1 < len(cmd_string):
                next_char = cmd_string[i + 1]
                if next_char == "\\" or next_char == '"':
                    current_args += next_char
                    i += 2
                    continue
                current_args += char
                i += 1
                continue

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
        error_mode = "w"

        # ---- Output redirection ----
        # FIX #1: every branch now checks there's actually a filename
        # after the operator, instead of assuming parts[redirect_index + 1] exists.
        if ">>" in parts:
            redirect_index = parts.index(">>")
            if redirect_index + 1 >= len(parts):
                print("syntax error: expected filename after '>>'", file=sys.stderr)
                continue
            output_file = parts[redirect_index + 1]
            output_mode = "a"
            parts = parts[:redirect_index]

        elif "1>>" in parts:
            redirect_index = parts.index("1>>")
            if redirect_index + 1 >= len(parts):
                print("syntax error: expected filename after '1>>'", file=sys.stderr)
                continue
            output_file = parts[redirect_index + 1]
            output_mode = "a"
            parts = parts[:redirect_index]

        elif ">" in parts:
            redirect_index = parts.index(">")
            if redirect_index + 1 >= len(parts):
                print("syntax error: expected filename after '>'", file=sys.stderr)
                continue
            output_file = parts[redirect_index + 1]
            output_mode = "w"
            parts = parts[:redirect_index]

        elif "1>" in parts:
            redirect_index = parts.index("1>")
            if redirect_index + 1 >= len(parts):
                print("syntax error: expected filename after '1>'", file=sys.stderr)
                continue
            output_file = parts[redirect_index + 1]
            output_mode = "w"
            parts = parts[:redirect_index]

        # ---- Error redirection ----
        if "2>>" in parts:
            redirect_index = parts.index("2>>")
            if redirect_index + 1 >= len(parts):
                print("syntax error: expected filename after '2>>'", file=sys.stderr)
                continue
            error_file = parts[redirect_index + 1]
            error_mode = "a"
            parts = parts[:redirect_index]

        elif "2>" in parts:
            redirect_index = parts.index("2>")
            if redirect_index + 1 >= len(parts):
                print("syntax error: expected filename after '2>'", file=sys.stderr)
                continue
            error_file = parts[redirect_index + 1]
            error_mode = "w"
            parts = parts[:redirect_index]

        if not parts:
            continue

        prog = parts[0]

        # ---- Open stdout ----
        # FIX #2: open() can raise (bad permissions, missing dir, etc) —
        # catch it instead of letting it crash the whole shell.
        if output_file:
            try:
                output = open(output_file, output_mode)
            except OSError as e:
                print(f"{output_file}: {e.strerror.lower()}", file=sys.stderr)
                continue
        else:
            output = sys.stdout

        # ---- Open stderr ----
        if error_file:
            try:
                error_output = open(error_file, error_mode)
            except OSError as e:
                print(f"{error_file}: {e.strerror.lower()}", file=sys.stderr)
                if output_file:
                    output.close()
                continue
        else:
            error_output = sys.stderr

        # FIX #4: try/finally guarantees these files close even if a builtin
        # or subprocess.run() throws partway through.
        try:

            if prog == "pwd":
                print(os.getcwd(), file=output)

            elif prog == "exit":
                break

            elif prog == "echo":
                print(" ".join(parts[1:]), file=output)

            elif prog == "cd":
                if len(parts) > 1:
                    target_path = parts[1]
                    if target_path == "~":
                        target_path = os.getenv("HOME")
                else:
                    target_path = os.getenv("HOME")

                try:
                    os.chdir(target_path)
                # FIX #3: was two identical except blocks — merged into one.
                # (added PermissionError/NotADirectoryError since those are
                # realistic cd failures too, same message for now)
                except (FileNotFoundError, TypeError, NotADirectoryError, PermissionError):
                    print(f"cd: {target_path}: No such file or directory", file=error_output)

            elif prog == "type":
                if len(parts) > 1:
                    subject = parts[1]
                    if subject in built_in_commands:
                        print(f"{subject} is a shell builtin", file=output)
                    elif path := shutil.which(subject):
                        print(f"{subject} is {path}", file=output)
                    else:
                        print(f"{subject}: not found", file=error_output)

            else:
                path = shutil.which(prog)
                if not path:
                    print(f"{prog}: command not found", file=error_output)
                else:
                    subprocess.run(parts, executable=path, stdout=output, stderr=error_output)

        finally:
            if output_file:
                output.close()
            if error_file:
                error_output.close()


if __name__ == "__main__":
    main()