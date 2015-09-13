from django.db import models

class Permalink(models.Model):

    class Meta:
        app_label = 'docs'

    name = models.CharField(max_length=256)
    file = models.ForeignKey('File', related_name='permalinks')
    revision = models.ForeignKey('Revision', null=True, related_name='permalinks')
    valid_since = models.DateTimeField(null=True)

    def __unicode__(self):
        if self.revision:
            return '%s (#%s +%d)' % (self.name, self.file.id, self.revision.id)
        else:
            return '%s (#%s)' % (self.name, self.file.id)
