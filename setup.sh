#!/bin/bash
set -eu
function ask {
    while true; do
	read -rp "$* [Y/N]: " a
	case $a in
        [Yy]*) return 0 ;; # Successful (true)
        [Nn]*) return 1 ;; # Failed (false)
      esac
    done
}


echo -e "Updating repositories...\n"
sudo apt-get update
echo ""

dependencies=(python3 python3-pip python3-venv)
echo "Checking if system dependencies are installed (if they are not, they're going to be installed AUTOMATICALLY with apt)"

for d in "${dependencies[@]}"; do
	echo -e "\n~ Checking if $d is installed"
	if dpkg-query -s "$d" >/dev/null 2>&1; then
		echo "It's installed!" 
	else
		echo -e "It isn't installed. \nInstalling...\n"
		if sudo apt-get install "$d" -y; then 
			echo -e "\nSuccessfully installed!" 
		else
			echo -e "\nAs you can see, there was a problem while trying to install the dependency \"$d\". Please make an issue with the output you just saw."
		fi
	fi
done

echo -e "\nChecking environment and required pip packages..."
if [ -d ".venv/" ]; then 
	echo "Environment already exists."
else
	echo "Creating environment..." 
	if python3 -m venv .venv; then 
		echo "Environment successfully created"
	else 
		echo "Couldn't create environment." 
		exit 1
	fi	
fi

echo -e "\nAutomatically checking and installing pip packages into the environment..."
.venv/bin/pip install -r requirements.txt

echo ""   
ask "Do you want to execute installer.py to proceed with the installation of your server?" && .venv/bin/python3 ./installer.py
echo ""
