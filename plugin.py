import os
import zipfile,tarfile

class Archiver():

	def __init__(self, main_window)	:
		self.main_window = main_window
		self.extract_mimes = ('application/zip','application/x-tar', 'application/x-compressed-tar')
		self.create_mimes = ('application/octet-stream')
		self.extract_menu = (
		{
		'label': 'Archiver',
		'submenu':
			(
			{
			'label': 'Extract',
			'data': False,
			'callback': self.extract,
			},
			{
			'label': 'Extract in folder',
			'data': True,
			'callback': self.extract,
			},
			)
		},
		)
		self.create_menu = (
		{
		'label': 'Archiver',
		'submenu':
			(
			{
			'label': 'Make archive',
			'callback': self.make_archive,
			},
			)
		},
		)


	def get_selection(self):
		selections = self.main_window.get_active_object()._get_selection()
		return selections

	def extract(self, widget, in_folder):
		filepath = self.get_selection()
		path = os.path.dirname(filepath)
		if in_folder :
			path = os.path.splitext(filepath)[0]

		try:
			if zipfile.is_zipfile(filepath):
				archive = zipfile.ZipFile(filepath)
			elif tarfile.is_tarfile(filepath):
				archive = tarfile.open(filepath)
			archive.extractall(path)
			archive.close()
		except Exception, e :
			print e

	def make_archive(self, widget, data):
		pass


def register_plugin(application):

	archiver = Archiver(application)

	for item in archiver.extract_menu:
		application.register_popup_menu_action(archiver.extract_mimes, application.menu_manager.create_menu_item(item))

