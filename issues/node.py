from issues.models import *

class IssueEntry(object):
	
	def __init__(self, id=None, model=None, user=None):
		if not model:
			if not id:
				raise TypeError("Must either specify issue # or provide model object")
			else:
				model = Issue.objects.get(id=id)

		self.model = model
		self.__user = user

	def title(self):
		pass

	def content(self):
		pass

	def edit(self, title=None, content=None):
		pass

	def comment(self, comment):
		pass

	def opened(self):
		pass

	def close(self, comment=None):
		pass

	def reopen(self, comment=None):
		pass

	def creator(self):
		pass

	def history(self):
		pass

	def last_updated(self):
		pass

	def assign(self, user):
		pass

	def assignee(self):
		return self.model.assignee

	def expired(self):
		pass

	def due(self):
		pass

	def set_due(self, due_time):
		pass

	def stargazers(self):
		pass

	def star(self):
		pass

	def unstar(self):
		pass

	def labels(self):
		pass

	def add_label(self, label):
		pass

	def remove_label(self, label):
		pass

class HistoryEntry(object):

	def __init__(self):
		pass
