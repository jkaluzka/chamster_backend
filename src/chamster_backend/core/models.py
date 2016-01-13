from django.db import models


class ProjectType(models.Model):
    # regular fields (1st field is id - default pk)
    name = models.CharField(max_length=128, unique=True)
    comments = models.CharField(max_length=256)

    class Meta:
        ordering = ['name']
        verbose_name = 'Project type'
        verbose_name_plural = 'Project types'

    def __unicode__(self):
        return unicode(self.name)


class Project(models.Model):
    # foreign keys
    project_type = models.ForeignKey('ProjectType', verbose_name='Project type')

    # regular fields (1st field is id - default pk)
    base_project = models.CharField(max_length=64)
    work_project = models.CharField(max_length=128)
    project_url = models.CharField(max_length=256)
    comments = models.CharField(max_length=256)

    class Meta:
        ordering = ['base_project', 'work_project', 'project_type']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        unique_together = (('base_project', 'work_project'),)

    def __unicode__(self):
        return unicode(self.base_project + '/' + self.work_project)

    @property
    def total_flows(self):
        return len(self.flow_set.all())

    @property
    def last_flow(self):
        return self.flow_set.order_by('-timestamp').first()

    @property
    def total_events(self):
        return sum((f.total_events for f in self.flow_set.all()))


class Flow(models.Model):
    # foreign keys
    project = models.ForeignKey('Project', verbose_name='Project')

    # regular fields (1st field is id - default pk)
    number = models.PositiveIntegerField()
    timestamp = models.DateTimeField('Flow timestamp')
    # TODO(brand0m): FlowStatus model and relation is needed here
    status = models.SmallIntegerField('Flow status')
    comments = models.CharField(max_length=256)

    class Meta:
        ordering = ['project', 'number']
        verbose_name = 'Flow'
        verbose_name_plural = 'Flows'
        unique_together = (('project', 'number'),)

    def __unicode__(self):
        return unicode(self.number)

    @property
    def total_events(self):
        return len(self.event_set.all())    # Event contains relationship to Flow

    @property
    def last_event(self):
        return self.event_set.order_by('-timestamp').first()


class EventType(models.Model):
    # regular fields (1st field is id - default pk)
    name = models.CharField(max_length=128, unique=True)
    comments = models.CharField(max_length=256)

    class Meta:
        ordering = ['name']
        verbose_name = 'Event type'
        verbose_name_plural = 'Event types'

    def __unicode__(self):
        return unicode(self.name)


class Event(models.Model):
    # foreign keys
    flow = models.ForeignKey('Flow', verbose_name='Flow')
    event_type = models.ForeignKey('EventType', verbose_name='Event type')

    # regular fields (1st field is id - default pk)
    timestamp = models.DateTimeField('Event time stamp')
    user = models.CharField(max_length=32)
    comments = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        unique_together = (('flow', 'event_type', 'timestamp'),)
