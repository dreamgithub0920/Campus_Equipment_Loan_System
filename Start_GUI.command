#!/bin/bash
# Open this file on macOS, or run: bash Start_GUI.command
cd -- "$(dirname -- "$0")" || exit 1

launch_if_supported() {
    local interpreter="$1"
    if "$interpreter" -c 'import sys; assert sys.version_info >= (3, 10); import tkinter' >/dev/null 2>&1; then
        "$interpreter" gui.py "${gui_arguments[@]}"
        return $?
    fi
    return 125
}

gui_arguments=("$@")
# Prefer a suitable user-installed Python. The final fallback supports this Mac's
# existing Codex Python runtime without requiring another installation.
for gui_python in python3.14 python3.13 python3.12 python3.11 python3.10 python3 \
    /opt/homebrew/bin/python3 /usr/local/bin/python3 \
    /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 \
    /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 \
    /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 \
    /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 \
    /Library/Frameworks/Python.framework/Versions/3.10/bin/python3 \
    "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"; do
    command -v "$gui_python" >/dev/null 2>&1 || continue
    launch_if_supported "$gui_python"
    gui_status=$?
    if [ "$gui_status" -ne 125 ]; then
        if [ "$gui_status" -ne 0 ]; then
            echo "The interface could not start. Review the message above."
            read -r -p "Press Return to close. "
        fi
        exit "$gui_status"
    fi
done

echo "Python 3.10 or newer with Tkinter is required."
echo "Install a Python distribution with Tk support, then open this file again."
read -r -p "Press Return to close. "
exit 1
