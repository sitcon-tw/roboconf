from docs.models import *
from docs.perms import is_in_scope

class Node(object):
	
	def __init__(self, nid=None, nodeobj=None, user=None):
		if not nodeobj:
			if not nid:
				raise TypeError('Must either specify NID or provide model instance')
			else:
				from django.utils.http import urlsafe_base64_decode
				nid = urlsafe_base64_decode(nidb64)
				if nid[-1:] == 'F':
					model = File
					self.__type = File
				elif nid[-1:] == 'D':
					model = Folder
					self.__type = Folder
				else:
					raise ValueError('Inappropriate NID type')

				nodeobj = model.objects.get(id=nid[:-1])
		else:
			if isinstance(nodeobj, File):
				self.__type = File
			elif isinstance(nodeobj, Folder):
				self.__type = Folder
			else:
				raise TypeError('Inappropriate model type')

		self.model = nodeobj
		self.__user = user

	def __perms(self):
		try:
			return self.__cached_perms
		except AttributeError:
			from docs.perms import get_perms
			self.__cached_perms = get_perms(self.__user, self.model)
			return self.__cached_perms

	def __filter_items(self, set):
		result = []
		for i in set:
			n = Node(nodeobj=i, user=self.__user)
			if n.can_view():
				result.append(n)
		return result

	def parent(self):
		return None if not self.model.parent else Node(nodeobj=self.model.parent, user=self.__user) 

	def is_file(self):
		return self.__type == File

	def is_folder(self):
		return self.__type == Folder

	def nid(self):
		from django.utils.encoding import force_bytes
		from django.utils.http import urlsafe_base64_encode
		return urlsafe_base64_encode(force_bytes(self.model.id) + force_bytes(self.__type.nid_namespace))

	def can_view(self):
		return Permission.VIEW in self.__perms()

	def can_comment(self):
		return Permission.COMMENT in self.__perms()

	def can_edit(self):
		return Permission.EDIT in self.__perms()

	def items(self):
		if self.is_file():
			return None

		from itertools import chain
		return self.__filter_items(chain(self.model.folders.all(), self.model.files.all()))

	def files(self):
		return None if self.is_file() else self.__filter_items(self.model.files.all())

	def folders(self):
		return None if self.is_file() else self.__filter_items(self.model.folders.all())

	def starred(self):
		return None if not self.__user else self.model.starred.filter(id=self.__user.id).exists()
