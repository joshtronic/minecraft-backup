#!/usr/bin/env python
#
# Name:    MineCraft Backup
# Author:  Josh Sherman <josh@gravityblvd.com>
# Website: https://github.com/joshtronic/minecraft-backup

import os.path
import threading
import subprocess
import shutil

# Configuration variables
minecraft_args = ["java", "-Xmx1024M", "-Xms512M", "-cp", "/home/josh/Desktop/Minecraft.jar", "net.minecraft.LauncherFrame"]
frequency      = 60
total_backups  = 10 
minecraft_path = os.environ["HOME"] + "/.minecraft/"
save_path      = minecraft_path + "saves/"
backup_path    = minecraft_path + "backups/"

# Check if the backup directory exists
if os.path.exists(backup_path) == False:
	os.mkdir(backup_path)

# World backup logic
def backupWorld(world):
	# Grabs the last modified time of the game save
	last_modified = str(os.path.getmtime(save_path + world))

	if os.path.exists(backup_path + world + "/" + last_modified) == False:
		shutil.copytree(save_path + world, backup_path + world + "/" + last_modified)

	# Purges old backups
	backups = sorted([d for d in os.listdir(backup_path + world) if os.path.isdir(backup_path + world + os.path.sep + d)])
	backups.extend(sorted([f for f in os.listdir(backup_path + world) if os.path.isfile(backup_path + world + os.path.sep + f)]))

	while len(backups) > total_backups:
		shutil.rmtree(backup_path + world + "/" + backups.pop(0))

# World backup logic
def runBackup():
	for i in range(1, 5):
		i     = str(i)
		world = "World" + i

		# Checks if world exists
		if os.path.exists(save_path + world):
			backupWorld(world)

	timer = threading.Timer(frequency, runBackup)
	timer.daemon = True
	timer.start()

runBackup();

# Launch MineCraft
subprocess.call(minecraft_args)

repeat_timer = False
