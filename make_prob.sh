#!/usr/bin/env bash

DIR=$(dirname "$0")

# 1. Configuration
TEMPLATE_DIR='.template'
PARENT_FILE='$PARENT'

# 2. Helper to find the template folder
search_up ()
(
    while [[ $PWD != "/" ]]; do
        if [[ -e "$1" ]]; then
            pwd
            if [[ ! -e "$1/$2" ]]; then
                break
            fi
        fi
        cd ..
    done
)

if command -v tac >/dev/null 2>&1; then
    REVERSE_CMD="tac"
else
    REVERSE_CMD="tail -r"
fi

# 4. Locate template directories
IFS=$'\n'
TEMPLATE_DIRS=($(search_up "$TEMPLATE_DIR" "$PARENT_FILE" | $REVERSE_CMD))
unset IFS
TEMPLATE_DIRS=(${TEMPLATE_DIRS[@]/%/\/"$TEMPLATE_DIR"})

# 5. Main Loop
for filepath in "$@"; do
    echo "Creating problem in: $filepath"

    if [[ -e "$filepath" ]]; then
        echo "  - Folder exists. Skipping."
        continue
    fi

    # Create the folder
    mkdir -p "$filepath"

    # Copy template files
    for CURRENT_TEMPLATE_DIR in "${TEMPLATE_DIRS[@]}"; do
        cp -R "$CURRENT_TEMPLATE_DIR/." "$filepath/"
    done
    rm -f "$filepath/$PARENT_FILE"

    if [[ -f "$filepath/template.cpp" ]]; then
        mv "$filepath/template.cpp" "$filepath/Solution.cpp"
        echo "  - Renamed template.cpp to Solution.cpp"
    fi
    # ---------------------------------------------

    # 6. Run setup script (if exists)
    pushd "$filepath" > /dev/null
    if [[ -e "setup" ]]; then
        echo "  - Running setup script"
        chmod +x setup
        ./setup
    fi
    popd > /dev/null
    
    echo "  - Done."
done
