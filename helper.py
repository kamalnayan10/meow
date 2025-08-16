import subprocess
import sys
import os
import textwrap

def get_directory_context():
    """
    gets the directory structure using 'tree' or falls back to 'ls'
    """
    try:
        result = subprocess.run(
            ["tree", "-L", "2"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            result = subprocess.run(
                ["find", ".", "-maxdepth", "2"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except Exception:
            return ""

def print_description_pretty(desc):
    """
    prints a description in a clean, word-wrapped format inside a
    dynamically sized box that fits the terminal.
    """
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    # --- create the dynamic box ---
    box_width = min(terminal_width, 100)
    
    top_bar = "╭" + "─" * (box_width - 2) + "╮"
    bottom_bar = "╰" + "─" * (box_width - 2) + "╯"
    
    title = "📝 Command Explanation"
    
    print("\n", file=sys.stderr)
    print(top_bar, file=sys.stderr)
    # center the title inside the box
    print(f"{title:^{box_width}}", file=sys.stderr)
    print(bottom_bar, file=sys.stderr)
    
    # --- configure the text wrapper ---
    wrap_width = box_width - 4 # 2 spaces of padding on each side
    
    initial_indent = "  • "
    subsequent_indent = "    "
    
    wrapper = textwrap.TextWrapper(
        width=wrap_width,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent
    )

    for line in desc:
        wrapped_text = wrapper.fill(line)
        print(wrapped_text, file=sys.stderr)
    
    print(file=sys.stderr)  # empty line for spacing

def print_cmd_pretty(command: str) -> str:
    """
    formats the generated command and instructions into a block with
    a style consistent with the description function.
    """
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80

    box_width = min(terminal_width, 80)
    
    # --- same as in description ---
    top_bar = "╭" + "─" * (box_width - 2) + "╮"
    bottom_bar = "╰" + "─" * (box_width - 2) + "╯"
    title = "🤖 AI Assistant - Generated Command"
    centered_title = f"{title:^{box_width}}"

    command_wrapper = textwrap.TextWrapper(
        width=box_width - 4,
        initial_indent="  • Command: ",
        subsequent_indent="            " # 12 spaces to align
    )
    wrapped_command = command_wrapper.fill(command)

    instructions_line = "  • Press Enter to execute (or edit and press Enter)"

    # --- assemble the final output string ---
    output_parts = [
        "",
        top_bar,
        centered_title,
        bottom_bar,
        "",
        wrapped_command,
        instructions_line,
        ""
    ]
    
    return "\n".join(output_parts)

        
if __name__ == "__main__":
    print(get_directory_context())
    print_description_pretty(["hello", "hi"])