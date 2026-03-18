#!/bin/bash

# 1. Infinite loop to wait for internet
echo "Waiting for internet..."
while ! ping -c 1 -W 1 8.8.8.8 > /dev/null; do
    sleep 5
done

# 2. Define your repo details
REPO_URL="https://github.com/azidav/redes-rasp-1.git"
REPO_DIR="/home/btk/redes-rasp-1"

# 3. Clone or Pull
if [ -d "$REPO_DIR" ]; then
    echo "Folder exists. Pulling latest code..."
    cd "$REPO_DIR"
    # If you made local changes to logs in this folder, 
    # 'git stash' ensures the 'pull' doesn't fail.
    git stash
    git pull
else
    echo "First time setup. Cloning public repo..."
    git clone "$REPO_URL" "$REPO_DIR"
    cd "$REPO_DIR"
fi

# 4. Launch the server
# --break-system-packages allows global Flask to run on newer Pi OS
echo "Starting Flask Server..."
python3 -u app.py >> /home/btk/server_output.log 2>&1