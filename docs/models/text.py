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

    FORMAT_ENUMERATION = (
            (TEXT, 'text'),
            (MARKDOWN, 'markdown'),
            (HTML, 'html'),
            (BLOB, 'blob'),
        )

    text = models.TextField()
    format = models.CharField(max_length=1, choices=FORMAT_CHOICES, default=TEXT)

    def __str__(self):
        return '%s (%d)' % (self.format, len(self.text))
