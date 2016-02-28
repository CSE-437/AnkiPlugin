import os, time, sys, time
from shutil import copy

watched_file = sys.argv[1]
addon_path = sys.argv[2]

os.startfile(r'C:\Program Files (x86)\Anki\anki.exe')

new_t = old_t = 0
while 1:
	old_t = new_t
	new_t = os.stat(watched_file)[8]
	if old_t != new_t:
		copy(watched_file, addon_path)
		os.system("TASKKILL /F /IM anki.exe")
		os.startfile(r'C:\Program Files (x86)\Anki\anki.exe')

	time.sleep(1);