sudo apt update
sudo apt install -y ca-certificates     curl     gnupg     lsb-release
sudo apt install -y python3.10-venv
sudo apt install -y make
sudo apt install -y gcc
sudo apt install -y python3-dev
sudo apt install -y libpq-dev
sudo apt install -y postgresql-common
sudo apt install -y libev-dev
sudo apt install -y system76-cuda-latest
sudo apt install -y nvidia-container-toolkit 
sudo apt install -y nvidia-docker2
sudo systemctl daemon-reload
sudo systemctl restart docker
