# 🐈 meow — Your AI Command-Line Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)](#)

**meow** translates your natural language into ready-to-execute shell commands — right in your terminal. Stop hunting for flags and syntax; just tell meow what you want.

https://github.com/user-attachments/assets/6b27ce87-2fa0-492a-8e5a-fcb6241a2470


![Demo Placeholder](docs/demo.gif)

---

## ✨ Features

- **Natural Language → Shell Commands**  
  Ask: _“find all files larger than 100MB”_ → meow prints:
  ~~~bash
  find . -type f -size +100M
  ~~~

- **Interactive Execution**  
  meow outputs the command in an editable prompt. Press **Enter** to run, or edit first.

- **Directory Context-Aware**  
  Uses your current directory to craft more accurate commands.

- **Verbose & Quiet Modes**  
  - Default: `--verbose` (explanations + command)  
  - Quiet: `--quiet` (command only)
 
- **Security by Design** 🔒  
  - Commands are **never auto-executed**.  
  - You always see what will run before execution.  
  - Explanations help you understand *why* the command is safe.

- **Beginner Friendly** 🐾  
  - Designed for developers transitioning into Linux/Unix.  
  - Explains unfamiliar commands in plain English.  
  - Makes the shell more approachable without sacrificing control.

---

## ⚙️ Installation

> meow installs by cloning a repo to `~/.meow` and adding a shell function.

### 1) Clone the Repository
~~~bash
git clone https://github.com/kamalnayan10/meow.git ~/.meow
~~~

### 2) Install Dependencies
~~~bash
cd ~/.meow
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
~~~

### 3) Configure Your API Key
Create a `.env` file with your **Gemini** API key:
~~~bash
touch ~/.meow/.env
~~~
~~~ini
# File: ~/.meow/.env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
~~~

### 4) Add the Shell Function

To make `meow` available as a command everywhere in your terminal, you need to add a function to your shell’s config file.

#### 1. Open your shell config file
- **Bash users:**  
  ```bash
  nano ~/.bashrc
- **Zsh users:**  
  ```bash
  nano ~/.zshrc

#### 2. Scroll to the bottom of the file
Move to the very end of the file and paste the following block of code:

``` bash
if [[ $- == *i* ]]; then

    # Function displays a spinner animation while response is loading
    _spinner() {
        # Define the animation frames as an array
        local frames=(
            "[ 🐈 .oO( m       )]"
            "[ 🐈 .oO( me      )]"
            "[ 🐈 .oO( meo     )]"
            "[ 🐈 .oO( meow    )]"
            "[ 🐈 .oO( meow .  )]"
            "[ 🐈 .oO( meow .. )]"
            "[ 🐈 .oO( meow ...)]"
        )
            
        # Hide the cursor
        echo -ne "\033[?25l"
        
        # Loop indefinitely
        while :; do
            # Loop through each frame in the array
            for frame in "${frames[@]}"; do
                # -ne allows use of \r (carriage return) to overwrite the line
                echo -ne "\r$frame"
                sleep 0.15
            done
        done
    }

    meow() {
        if [[ "$1" == "-h" || "$1" == "--help" ]]; then
            # If it is, just run the Python script with that flag and stop.
            ~/.meow/meow "$@"
            return
        fi
        
        _spinner &
        local spinner_pid=$!
        
        # disown the spinner
        disown

        local cmd
        # run python script with the prompt
        cmd=$(~/.meow/meow "$@")
        
        kill "$spinner_pid" 2>/dev/null
        wait "$spinner_pid" 2>/dev/null
        
        # clear the spinner line and show cursor
        echo -ne "\r\033[K\033[?25h"
        
        # create a proper prompt that looks like the user's actual prompt
        local user_prompt="${USER}@${HOSTNAME}:${PWD/#$HOME/~}\$ "
        
        # use read with the proper prompt format
        read -e -i "$cmd" -p "$user_prompt" final_cmd
        
        # execute if user pressed enter (or modified and pressed enter)
        if [[ -n "$final_cmd" ]]; then
            echo
            echo "  • 🖥️ Executing: $final_cmd"
            eval "$final_cmd"
            echo 
            echo "  • ✅ Command Executed Successfully"
        else
            echo "  • ⚠️ Cancelled"
        fi
        echo
    }
fi
```

### 5) Reload Your Shell
~~~bash
# Bash
source ~/.bashrc

# Zsh
source ~/.zshrc
~~~

---

## 🚀 Usage

Standard (verbose):
~~~bash
meow find all files larger than 100MB
~~~

Quiet mode (command only):
~~~bash
meow -q show me the current git branch
~~~

With punctuation/quotes:
~~~bash
meow "unzip 'archive.zip' and then delete it"
~~~

Help:
~~~bash
meow --help
~~~

---

## 🛣️ Roadmap

- [ ] Transition to a fully local open-source model (no API key).
- [ ] Publish official `.deb` package (APT install).

---

## ❓ FAQ

**Does meow auto-run commands?**  
No. It prints the command in an editable prompt. You choose to run it by pressing **Enter**.

**Which shells are supported?**  
Bash and Zsh (the provided function targets interactive shells).

**Where is the binary/script?**  
Expected at `~/.meow/meow`. Adjust the function if you place it elsewhere.

---

## 🤝 Contributing

PRs welcome! If you add features (e.g., different models, local LLM, or richer explanations), include docs and a short demo clip.

---

## 📄 License

Licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
