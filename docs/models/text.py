from django.db import models

class BlobText(models.Model):

	class Meta:
		app_label = 'docs'

	TEXT = ' '
	MARKDOWN = 'M'
	HTML = '<'
	BLOB = 'B'

	FORMAT_CHOICES = (
			(TEXT, 'Plain text'),
			(MARKDOWN, 'Markdown text'),
			(HTML, 'HTML document'),
			(BLOB, 'Binary content'),
		)

	text = models.TextField()
	format = models.CharField(max_length=1, choices=FORMAT_CHOICES, default=TEXT)

	def __unicode__(self):
		return '%s (%d)' % (self.format, len(self.text))
