import os
import gtk
import zipfile,tarfile

class Archiver():

	def __init__(self, main_window)	:
		self.main_window = main_window
		self.archive_mimes = ('application/zip', 'application/x-tar', 'application/x-compressed-tar')
		self.menu_mimes = ('application/octet-stream', 'inode/directory', 'text/directory', 'folder')
		self.extract_menu_item = (
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

		self.extract_menu = gtk.Menu()
		for item in self.extract_menu_item:
			self.extract_menu.append(self.main_window.menu_manager.create_menu_item(item))


		self.create_menu_item = (
			{
				'label': 'Make archive',
				'callback': self.make_archive,
			},
		)

		self.create_menu = gtk.Menu()
		for item in self.create_menu_item:
			self.create_menu.append(self.main_window.menu_manager.create_menu_item(item))

		self.archiver_menu = self.main_window.menu_manager.create_menu_item(
			{
				'label': 'Archiver',
				'submenu': ''
			}
		)
		self.archiver_menu.connect("activate", self.expand_menu)

	def expand_menu(self, data):
		self.archiver_menu.set_submenu(self.create_menu)
		filename = self.get_selection()

		try:
			if zipfile.is_zipfile(filename) or tarfile.is_tarfile(filename):
					self.archiver_menu.set_submenu(self.extract_menu)
		except IOError as e:
			if e.errno == 21:
				pass

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
		filepath = self.get_selection()
		zfile = filepath.rstrip('/') + '.zip'
		filepath = filepath.rstrip('/')
		zf = zipfile.ZipFile(zfile, mode='w')
		if os.path.isfile(filepath):
			zf.write(filepath, filepath[len(os.path.dirname(filepath)):].strip('/'), compress_type=zipfile.ZIP_DEFLATED)
		else:
			for root, dirs, files in os.walk(filepath):
				for name in files:
					file_to_zip = os.path.join(root, name)
					arcname = file_to_zip[len(os.path.dirname(filepath)):].strip('/')
					zf.write(file_to_zip, arcname, compress_type=zipfile.ZIP_DEFLATED)


def register_plugin(application):
	archiver = Archiver(application)
	application.register_popup_menu_action(archiver.menu_mimes, archiver.archiver_menu)

