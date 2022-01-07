import configparser
import os
from pathlib import Path

# Log in a user first

home = str(Path.home())
ini = home + "/pyfi.ini"

CONFIG = configparser.ConfigParser()
if CONFIG.has_section("login"):
    user = CONFIG.get("login", "user")
    password = CONFIG.get("login", "password")

if os.path.exists(ini):
    CONFIG.read(ini)
