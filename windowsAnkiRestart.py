import os, time, sys, time, subprocess
from shutil import copy

paths_file = open('ankiRestartPaths.txt')
paths = []
for path in paths_file:
	paths.append(path.replace("\n", ""))

anki_exe = paths[0]
watched_files = paths[1]
addon_path = paths[2]
kill_cmd = paths[3]

os.startfile(anki_exe)

new_t = old_t = 0
while 1:
	didcopy = False
	for watched_file in watched_files.split(','):
		old_t = new_t
		new_t = os.stat(watched_file)[8]
		if old_t != new_t:
			copy(watched_file, addon_path)
			didcopy = True
	if didcopy:
		os.system(kill_cmd)
		os.startfile(anki_exe)
		result = subprocess.check_output(anki_exe, shell=True)

	time.sleep(1);
