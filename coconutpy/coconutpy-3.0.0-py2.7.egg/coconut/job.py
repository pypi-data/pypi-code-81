import coconut
from coconut import api

class Job:
  @classmethod
  def apply_settings(self, job):
    if coconut.webhook_url is not None:
      if job.get('webhook') is None:
        job['webhook'] = {}

      job['webhook'].update({'url': coconut.webhook_url})

    if coconut.storage is not None:
      if job.get('storage') is None:
        job['storage'] = {}

      job['storage'].update(coconut.storage)

    return job

  @classmethod
  def retrieve(self, job_id, **kwargs):
    return api.request('GET', '/jobs/' + job_id, **kwargs)

  @classmethod
  def create(self, job, **kwargs):
    return api.request('POST', '/jobs', json=self.apply_settings(job), **kwargs)