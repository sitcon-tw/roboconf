from docs.models import *

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
		self.__parent = None

	def __direct_acl(self):
		return sorted(self.model.permissions.all(), key=Permission.__key__, reverse=True)

	def __acl(self):
		if self.__cached_acl:
			return self.__cached_acl
		else:
			if self.parent():
				from itertools import chain
				self.__cached_acl = tuple(chain(self.__direct_acl(), self.__parent.__acl()))
			else:
				self.__cached_acl = self.__acl()
			return self.__cached_acl

	def __perms(self):
		try:
			return self.__cached_perms
		except AttributeError:
			from docs.perms import *
			max_perm = PRIORITY_COUNT - 1
			cur_perm = -1

			for perm in self.__acl():
				priority = PRIORITY_MAPPING[perm.type]

				if is_in_scope(self.__user, perm):

					if perm.effect == Permission.ALLOW:
						cur_perm = min(max(priority, cur_perm), max_perm)

					elif perm.effect == Permission.DENY:
						max_perm = min(priority, max_perm) - 1
						if cur_perm > max_perm:
							break		# We can't acquire more permissions upstream

			self.__cached_perms = PRIORITY[:cur_perm+1]
			return self.__cached_perms

	def __filter_items(self, set):
		result = []
		for i in set:
			n = Node(nodeobj=i, user=self.__user)
			if n.can_view():
				result.append(n)
		return result

	def parent(self):
		if not self.__parent:
			if not self.model.parent:
				return None
			else:
				self.__parent = Node(nodeobj=self.model.parent, user=self.__user)
				return self.__parent
		return self.__parent

	def is_file(self):
		return self.__type == File

	def is_folder(self):
		return self.__type == Folder

	def id(self):
		return self.model.id

	def nid(self):
		from django.utils.encoding import force_bytes
		from django.utils.http import urlsafe_base64_encode
		return urlsafe_base64_encode(force_bytes(self.model.id) + force_bytes(self.__type.nid_namespace))

	def name(self):
		return self.model.name

	def last_modified(self):
		return self.model.last_modified

	def last_editor(self):
		return None if self.is_folder() else self.model.current_revision.user

	def path(self):
		node = self
		path = [self]
		while node.model.parent:
			node = node.parent()
			path.append(node)
		path.reverse()
		return path

	def can_view(self):
		return Permission.VIEW in self.__perms()

	def can_comment(self):
		return Permission.COMMENT in self.__perms()

	def can_edit(self):
		return Permission.EDIT in self.__perms()

	def empty(self):
		return not self.model.files.exists() and not self.model.folders.exists()

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
