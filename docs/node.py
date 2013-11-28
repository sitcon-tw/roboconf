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

		self.__obj = nodeobj
		self.__user = user

	def model(self):
		return self.__obj

	def parent(self):
		return None if not self.__obj.parent else Node(nodeobj=self.__obj.parent, user=self.__user) 

	def is_file(self):
		return self.__type == File

	def is_folder(self):
		return self.__type == Folder

	def nid(self):
		from django.utils.encoding import force_bytes
		from django.utils.http import urlsafe_base64_encode
		return urlsafe_base64_encode(force_bytes(self.__obj.id) + force_bytes(self.__type.nid_namespace))

	def can_view(self):
		pass

	def can_comment(self):
		pass

	def can_edit(self):
		pass

	def items(self):
		if self.is_file():
			return None
		pass

	def files(self):
		if self.is_file():
			return None
		pass

	def folders(self):
		if self.is_file():
			return None
		pass

	def starred(self):
		return None if not self.__user else self.__obj.starred.filter(id=self.__user.id).exists()
