important: install tree on your linux system to get better results
sudo apt install tree

this needs to be pasted in ~/.bashrc

# cli tool assistant

```
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
