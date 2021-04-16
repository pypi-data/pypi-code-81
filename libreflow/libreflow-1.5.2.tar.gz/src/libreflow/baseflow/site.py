import os
import sys
import gazu
import time
from datetime import datetime, timedelta
import subprocess
import platform
from minio import Minio
import zipfile
import fnmatch
import re

from kabaret import flow
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict
from kabaret.subprocess_manager.flow import RunAction

from .maputils import ItemMap, CreateGenericAction, ClearMapAction, RemoveGenericAction
from libreflow.baseflow.runners import BaseRunner, PythonRunner


class StaticSiteTypeChoices(flow.values.ChoiceValue):
    CHOICES = ['Studio', 'User']


class StaticSiteSyncStatusChoices(flow.values.ChoiceValue):
    CHOICES = ['NotAvailable', 'Requested', 'Available']


class StaticSiteSyncTransferStateChoices(flow.values.ChoiceValue):
    CHOICES = ['NC', 'UP_REQUESTED', 'DL_REQUESTED', 'UP_IN_PROGRESS', 'DL_IN_PROGRESS']


class LoadType(flow.values.ChoiceValue):

    CHOICES = ['Upload', 'Download']


class JobStatus(flow.values.ChoiceValue):

    CHOICES = ['WFA', 'WAITING', 'PROCESSED', 'ERROR', 'PAUSE', 'DONE']


class Job(flow.Object):

    type = flow.Param('Download', LoadType)
    status = flow.Param('WAITING', JobStatus)
    priority = flow.IntParam(50)
    emitter_oid = flow.Param()
    date = flow.Param("").ui(editor='datetime')
    date_end = flow.Param("").ui(editor='datetime')
    is_archived = flow.BoolParam()
    requested_by_user = flow.Param()
    requested_by_studio = flow.Param()
    log = flow.Param().ui(editor='textarea')

    def __repr__(self):
        job_repr = "%s(type=%s, status=%s, priority=%s, emitter=%s, date=%s, date_end=%s, is_archived=%s, requested_by_user=%s, requested_by_studio=%s)" % (
                self.__class__.__name__,
                self.type.get(),
                self.status.get(),
                self.priority.get(),
                self.emitter_oid.get(),
                self.date.get(),
                self.date_end.get(),
                self.is_archived.get(),
                self.requested_by_user.get(),
                self.requested_by_studio.get()
            )

        return job_repr


class JobQueue(flow.Map):

    @classmethod
    def mapped_type(cls):
        return Job
    
    def get_next_waiting_job(self):
        for job in reversed(self.mapped_items()):
            if job.status.get() == "WAITING":
                return job
        
        return None
    
    def jobs(self, type=None, status=None):
        jobs = self.mapped_items()

        if type:
            jobs = list(filter(lambda job: job.type.get() == type, jobs))
        if status:
            jobs = list(filter(lambda job: job.status.get() == status, jobs))
        
        return jobs
    
    def insert(self, name, priority=0):
        """
        Inserts a new job with given name and priority.
        """
        job = self.add(name)
        self._mapped_names.set_score(name, priority)

        return job
    
    def submit_job(self,
            emitter_oid,
            user,
            studio,
            date_end=-1,
            job_type='Download',
            init_status='WAITING',
            priority=50
        ):
        
        name = '%s_%s_%s_%i' % (
            emitter_oid[1:].replace('/', '_'),
            studio,
            job_type,
            time.time()
        )
        job = self.insert(name, priority)

        job.type.set(job_type)
        job.status.set(init_status)
        job.priority.set(priority)
        job.emitter_oid.set(emitter_oid)
        job.date.set(time.time())
        job.date_end.set(date_end)
        job.requested_by_user.set(user)
        job.requested_by_studio.set(studio)
        job.is_archived.set(False)
        job.log.set('?')

        self.root().session().log_info("Submitted job %s" % job)

        self.touch()

        return job
    
    def columns(self):
        return [
            "Type",
            "Status",
            "Priority",
            "Emitted on",
            "Expires on",
            "Requested by (site/user)",
        ]
    
    def _fill_row_cells(self, row, item):
        row["Type"] = item.type.get()
        row["Status"] = item.status.get()
        row["Priority"] = item.priority.get()
        row["Emitted on"] = datetime.fromtimestamp(item.date.get()).ctime()
        row["Expires on"] = "Never" if item.date_end.get() == -1 else item.date_end.get()
        row["Requested by (site/user)"] = "%s/%s" % (
            item.requested_by_studio.get(),
            item.requested_by_user.get()
        )


class ProcessJobs(flow.Action):

    def needs_dialog(self):
        return False

    def _process(self, job):
        raise NotImplementedError(
            "Must be implemented to process the given job"
        )
    
    def _get_jobs(self):
        current_site = self.root().project().get_current_site()
        return current_site.get_jobs()
    
    def run(self, button):
        for job in self._get_jobs():
            self.root().session().log_info("Processing job %s" % job)
            self._process(job)


class MinioFileUploader(PythonRunner):
    
    def argv(self):
        args = ["%s/../scripts/minio_file_uploader.py" % (
            os.path.dirname(__file__)
        )]
        args += self.extra_argv
        return args


class MinioFileDownloader(PythonRunner):
    
    def argv(self):
        args = ["%s/../scripts/minio_file_downloader.py" % (
            os.path.dirname(__file__)
        )]
        args += self.extra_argv
        return args


class MinioUploadFile(flow.Object):

    def upload(self, local_path, server_path):
        self.root().session().log_info(
            "Uploading file %s -> %s" % (
                local_path,
                server_path
            )
        )
        exchange_site = self.root().project().get_exchange_site()
        minioClient = Minio(
            exchange_site.server_url.get(),
            access_key=exchange_site.server_login.get(),
            secret_key=exchange_site.server_password.get(),
            secure=True
        )

        minioClient.fput_object(
            "testbucked",
            server_path,
            local_path
        )


class MinioDownloadFile(flow.Object):

    def download(self, server_path, local_path):
        self.root().session().log_info(
            "Downloading file %s -> %s" % (
                server_path,
                local_path
            )
        )
        exchange_site = self.root().project().get_exchange_site()
        minioClient = Minio(
            exchange_site.server_url.get(),
            access_key=exchange_site.server_login.get(),
            secret_key=exchange_site.server_password.get(),
            secure=True
        )

        minioClient.fget_object(
            "testbucked",
            server_path,
            local_path
        )

        if os.path.splitext(local_path)[1] == ".zip":
            # Unzip
            with zipfile.ZipFile(local_path, 'r') as zip_wc:
                zip_wc.extractall(os.path.dirname(local_path))


class Synchronize(ProcessJobs):

    uploader = flow.Child(MinioUploadFile).ui(hidden=True)
    downloader = flow.Child(MinioDownloadFile).ui(hidden=True)

    def _get_jobs(self):
        # Get current site's waiting jobs only
        current_site = self.root().project().get_current_site()
        return current_site.get_jobs(status="WAITING")

    def _get_sync_status(self, revision_oid, site_name=None, site_type="Studio"):
        if not site_name and site_type == "Exchange":
            exchange_site = self.root().project().get_exchange_site()
            if exchange_site:
                site_name = exchange_site.name()
            else:
                return "NotAvailable"

        sync_status = self.root().session().cmds.Flow.call(
            revision_oid, "get_sync_status",
            args={}, kwargs=dict(site_name=site_name)
        )
        return sync_status

    def _set_sync_status(self, revision_oid, status, site_name=None, site_type="Studio"):
        if not site_name and site_type == "Exchange":
            exchange_site = self.root().project().get_exchange_site()
            if exchange_site:
                site_name = exchange_site.name()
            else:
                self.root().session().log_error(
                    "No registered exchange site on this project !"
                )
                return

        self.root().session().cmds.Flow.call(
            revision_oid, "set_sync_status",
            args={status}, kwargs=dict(site_name=site_name)
        )
    
    def _touch(self, oid):
        oid = self.root().session().cmds.Flow.resolve_path(oid)
        self.root().session().cmds.Flow.call(
            oid, "touch", args={}, kwargs={}
        )

    def _process(self, job):
        if job.status.get() == "PROCESSED":
            self.root().session().log_warning(
                "Job %s already processed !" % job.name()
            )
            return

        local_path = self.root().session().cmds.Flow.call(
            job.emitter_oid.get(),
            "get_path",
            args={},
            kwargs={}
        )
        server_path = self.root().session().cmds.Flow.call(
            job.emitter_oid.get(),
            "get_relative_path",
            args={},
            kwargs={}
        )
        local_path = local_path.replace("\\", "/")
        server_path = server_path.replace("\\", "/")

        if job.type.get() == "Upload":
            if not os.path.exists(local_path):
                self.root().session().log_error((
                    "Following file requested for upload but does not exist !"
                    "\n>>>>> %s" % local_path
                ))
                return

            self.uploader.upload(local_path, server_path)
            self._set_sync_status(job.emitter_oid.get(), "Available", site_type="Exchange")
            self._touch(job.emitter_oid.get() + "/..")
        elif job.type.get() == "Download":
            sync_status = self._get_sync_status(job.emitter_oid.get(), site_type="Exchange")
            
            if sync_status != "Available":
                self.root().session().log_error((
                    "Following file requested for download "
                    "but not available on any exchange server !"
                    "\n>>>>> %s" % local_path
                ))
                return

            self.downloader.download(server_path, local_path)
            self._set_sync_status(job.emitter_oid.get(), "Available")
            self._touch(job.emitter_oid.get() + "/..")
            self._touch(job.emitter_oid.get() + "/../../../..")
        
        job.status.set("PROCESSED")
        
        # Refresh project's sync section UI
        self.root().project().synchronization.touch()


class RequestedSiteChoiceValue(flow.values.ChoiceValue):
    _revision = flow.Parent(2)

    def choices(self):
        site_names = []
        
        for site in self._revision.sync.mapped_items():
            if site.status.get() == "Available":
                site_names.append(site.name())
        
        return site_names


class RequestingSiteChoiceValue(flow.values.ChoiceValue):
    _revision = flow.Parent(2)

    def choices(self):
        site_names = []
        
        for site in self._revision.sync.mapped_items():
            if site.status.get() == "NotAvailable":
                site_names.append(site.name())
        
        return site_names


class RequestAs(flow.Action):

    _revision = flow.Parent()
    priority = flow.IntParam(50)
    requesting_site_name = flow.Param(None, RequestingSiteChoiceValue).ui(label="Requesting site")
    requested_site_name = flow.Param(None, RequestedSiteChoiceValue).ui(label="Site to query")

    def get_buttons(self):
        site_names = self.requested_site_name.choices()
        # Actually, an existing revision implies there is at least one
        # site on which it is available, which is the source site
        self.requested_site_name.set(site_names[0])

        return ["Request", "Cancel"]
    
    def allow_context(self, context):
        return (
            context
            and not self._revision.is_working_copy()
            and self.root().project().get_current_site().request_files_from_anywhere.get()
        )

    def run(self, button):
        if button == "Cancel":
            return
        
        requesting_site_name = self.requesting_site_name.get()

        # Get requesting and requested sites
        sites = self.root().project().get_working_sites()
        requesting_site = sites[requesting_site_name]
        
        # Add a download job for the requesting site
        requesting_site.get_queue().submit_job(
            job_type="Download",
            init_status="WAITING",
            emitter_oid=self._revision.oid(),
            user=self.root().project().get_user(),
            studio=requesting_site_name,
            priority=self.priority.get(),
        )
        self._revision.set_sync_status("Requested", site_name=requesting_site_name)
        self._revision._revisions.touch()
        
        # Check if the version is not available on the exchange server
        exchange_site = self.root().project().get_exchange_site()
        revision_status = self._revision.get_sync_status(exchange=True)

        if revision_status == "Available":
            self.root().session().log_warning(
                "Revision already available on exchange server"
            )
            self.root().project().synchronization.touch()
            return self.get_result()

        requested_site = sites[self.requested_site_name.get()]

        # Check if the source version upload is not already requested
        for job in requested_site.get_jobs(type="Upload", status="WAITING"):
            if job.emitter_oid.get() == self._revision.oid():
                self.root().session().log_warning(
                    "Revision already requested for upload in source site"
                )
                self.root().project().synchronization.touch()
                return self.get_result()
        
        # Add an upload job for the requested site
        requested_site.get_queue().submit_job(
            job_type="Upload",
            init_status="WAITING",
            emitter_oid=self._revision.oid(),
            user=self.root().project().get_user(),
            studio=requesting_site_name,
            priority=self.priority.get(),
        )

        # Refresh project's sync section UI
        self.root().project().synchronization.touch()


class Request(RequestAs):

    _revision = flow.Parent()
    priority = flow.IntParam(50)
    requesting_site_name = flow.Param("").ui(hidden=True)

    def get_buttons(self):
        self.requesting_site_name.set(
            self.root().project().get_current_site().name()
        )

        return super(Request, self).get_buttons()
    
    def allow_context(self, context):
        return (
            context
            and not self._revision.is_working_copy()
            and not self._revision.get_sync_status() == "Available"
        )


class ResetJobStatuses(flow.Action):
    _site = flow.Parent()
    status = flow.Param("WAITING", JobStatus)

    def run(self, button):
        for job in self._site.get_jobs():
            job.status.set(self.status.get())
        
        self._site.get_queue().touch()


class CreateSite(flow.Action):

    ICON = ("icons.gui", "plus-sign-in-a-black-circle")

    _site_map = flow.Parent()
    site_name = flow.SessionParam("").ui(label="Name")

    def get_buttons(self):
        self.message.set("<h2>Create a site</h2>")
        return ["Create", "Cancel"]
    
    def run(self, button):
        if button == "Cancel":
            return
        
        site_name = self.site_name.get()

        if not site_name or self._site_map.has_mapped_name(site_name):
            if not site_name:
                msg = "Site name must not be empty."
            else:
                msg = f"Site {site_name} already exists."

            self.message.set((
                "<h2>Create a site</h2>"
                f"<font color=#D5000D>{msg}</font>"
            ))
            
            return self.get_result(close=False)

        site = self._site_map.add(site_name)
        self._site_map.touch()

        return self.get_result(next_action=site.configuration.oid())


class ConfigureSite(flow.Action):

    _site_map = flow.Parent(2)
    _site = flow.Parent()
    short_name = flow.SessionParam("").ui(label="Short name")
    description = flow.SessionParam("")

    def get_buttons(self):
        self.message.set(
            "<h2>Site <font color=#fff>%s</font></h2>" % self._site.name()
        )
        self._fill_action_fields()

        return ["Configure", "Cancel"]

    def _configure_site(self, site):
        '''
        This can be used by subclass to configure a mapped site.

        Default is to set site's short name and description.
        '''
        self._site.short_name.set(self.short_name.get())
        self._site.description.set(self.description.get())
    
    def _fill_action_fields(self):
        '''
        This can be used by subclass to fill action's parameters when
        dialog is displayed (e.g. to automatically show site parameters).

        Default is to fill site's short name and description.
        '''
        self.short_name.set(self._site.short_name.get())
        self.description.set(self._site.description.get())
    
    def allow_context(self, context):
        # Hide in map item submenus
        return False
    
    def run(self, button):
        if button == "Cancel":
            return
        
        self._configure_site(self._site)
        self._site.configured.touch()
        self._site_map.touch()


class ComputedBoolValue(flow.values.ComputedValue):

    DEFAULT_EDITOR = 'bool'


class Site(flow.Object):

    short_name = flow.Param("")
    description = flow.Param("")
    # Define conditions required for a site to be considered as correctly configured
    configured = flow.Computed(
        cached=True,
        store_value=True,
        computed_value_type=ComputedBoolValue
    )
    configuration = flow.Child(ConfigureSite)

    def compute_child_value(self, child_value):
        if child_value is self.configured:
            self.configured.set(True)


class SiteMap(flow.Map):

    create_site = flow.Child(CreateSite)

    @classmethod
    def mapped_type(cls):
        return Site

    def mapped_names(self, page_num=0, page_size=None):
        return ["default"] + super(SiteMap, self).mapped_names(page_num, page_size)
    
    def columns(self):
        return ["Site"]
    
    def short_names(self):
        return [s.short_name.get() for s in self.mapped_items()]
    
    def _get_mapped_item_type(self, mapped_name):
        if mapped_name == "default":
            return self.mapped_type()

        return super(SiteMap, self)._get_mapped_item_type(mapped_name)
    
    def _fill_row_cells(self, row, item):
        row["Site"] = item.name()
        if not item.configured.get():
            row["Site"] += " ⚠️"
    
    def _fill_row_style(self, style, item, row):
        style["activate_oid"] = item.configuration.oid()


class ConfigureWorkingSite(ConfigureSite):

    site_type = flow.Param("Studio", StaticSiteTypeChoices)

    root_windows_folder = flow.SessionParam("")
    root_linux_folder = flow.SessionParam("")
    root_darwin_folder = flow.SessionParam("")
    
    sync_dl_max_connections = flow.SessionParam(1)
    sync_up_max_connections = flow.SessionParam(1)
    
    def _fill_action_fields(self):
        super(ConfigureWorkingSite, self)._fill_action_fields()
        self.site_type.set(self._site.site_type.get())
        self.root_windows_folder.set(self._site.root_windows_folder.get())
        self.root_linux_folder.set(self._site.root_linux_folder.get())
        self.root_darwin_folder.set(self._site.root_darwin_folder.get())
        self.sync_dl_max_connections.set(self._site.sync_dl_max_connections.get())
        self.sync_up_max_connections.set(self._site.sync_up_max_connections.get())

    def _configure_site(self, site):
        super(ConfigureWorkingSite, self)._configure_site(site)
        site.site_type.set(self.site_type.get())
        site.root_windows_folder.set(self.root_windows_folder.get())
        site.root_linux_folder.set(self.root_linux_folder.get())
        site.root_darwin_folder.set(self.root_darwin_folder.get())
        site.sync_dl_max_connections.set(self.sync_dl_max_connections.get())
        site.sync_up_max_connections.set(self.sync_up_max_connections.get())


class Queue(flow.Object):

    job_list = flow.Child(JobQueue).ui(label="Jobs", expanded=True)


class GotoQueue(flow.Action):

    _site = flow.Parent()

    def needs_dialog(self):
        return False
    
    def run(self, button):
        return self.get_result(goto=self._site.queue.oid())


class ClearQueueJobStatus(flow.values.ChoiceValue):

    CHOICES = JobStatus.CHOICES + ["All"]


class ClearQueueLoadType(flow.values.ChoiceValue):

    CHOICES = LoadType.CHOICES + ["All"]


class ClearQueueAction(flow.Action):

    _site = flow.Parent()
    status = flow.Param("PROCESSED", ClearQueueJobStatus)
    type = flow.Param("All", ClearQueueLoadType)
    emitted_before = flow.SessionParam((datetime.now() - timedelta(days=1)).timestamp()).ui(
        editor='datetime'
    )

    def get_buttons(self):
        self.message.set(
            "<h2>Clear %s jobs</h2>" % self._site.name()
        )
        return ["Clear", "Cancel"]
    
    def run(self, button):
        queue = self._site.get_queue()
        status = self.status.get()
        type = self.type.get()

        if status == "All" and type == "All":
            queue.clear()
        else:
            for job in queue.jobs(status=self.status.get()):
                if job.date.get() < self.emitted_before.get():
                    queue.remove(job.name())

        queue.touch()


class WorkingSite(Site):
    
    site_type = flow.Param("Studio", StaticSiteTypeChoices)
    request_files_from_anywhere = flow.BoolParam(False).ui(
        tooltip=(
            "Allow the site to request files for any other site. "
            "Temporary option as long as synchronisation is manual."
        )
    )

    root_folder = flow.Computed(cached=True)
    root_windows_folder = flow.Param()
    root_linux_folder = flow.Param()
    root_darwin_folder = flow.Param()
    
    sync_dl_max_connections = flow.IntParam(1)
    sync_up_max_connections = flow.IntParam(1)

    queue = flow.Child(Queue)

    configuration = flow.Child(ConfigureWorkingSite)
    goto_queue = flow.Child(GotoQueue).ui(
        label="Show job queue"
    )
    clear_queue = flow.Child(ClearQueueAction)

    def compute_child_value(self, child_value):
        if child_value is self.root_folder:
            root_dir = None
            # Get the operative system
            _os = platform.system()
            if _os == "Linux":
                root_dir = self.root_linux_folder.get()
            elif _os == "Windows":
                root_dir = self.root_windows_folder.get()
            elif _os == "Darwin":
                root_dir = self.root_darwin_folder.get()
            else:
                print("ERROR: Unrecognized operative system ?")
            
            if not root_dir or not os.path.exists(root_dir):
                print("WARNING: ROOT_DIR path DOES NOT EXISTS")

            child_value.set(root_dir)

        elif child_value is self.configured:
            self.configured.set(
                (
                    self.root_windows_folder.get()
                    or self.root_linux_folder.get()
                    or self.root_darwin_folder.get()
                )
            )
    
    def get_queue(self):
        return self.queue.job_list
    
    def get_jobs(self, type=None, status=None):
        return self.get_queue().jobs(type=type, status=status)


class WorkingSites(SiteMap):

    ICON = ('icons.gui', 'home')

    @classmethod
    def mapped_type(cls):
        return WorkingSite

    def _configure_child(self, child):
        if child.name() == "default":
            child.short_name.set("dft")
            child.description.set("Default working site")
            child.site_type.set("Studio")
        else:
            super(WorkingSites, self)._configure_child(child)

    def _fill_row_style(self, style, item, row):
        super(WorkingSites, self)._fill_row_style(style, item, row)

        if item.site_type.get() == "User":
            style['icon'] = ('icons.gui', 'user')
        else:
            style['icon'] = ('icons.gui', 'home')


class ConfigureExchangeSite(ConfigureSite):

    server_url = flow.SessionParam("http://")
    server_login = flow.SessionParam("")
    server_password = flow.SessionParam("").ui(editor='password')

    def _fill_action_fields(self):
        super(ConfigureExchangeSite, self)._fill_action_fields()
        self.server_url.set(self._site.server_url.get())
        self.server_login.set(self._site.server_login.get())
        self.server_password.set(self._site.server_password.get())

    def _configure_site(self, site):
        super(ConfigureExchangeSite, self)._configure_site(site)
        site.server_url.set(self.server_url.get())
        site.server_login.set(self.server_login.get())
        site.server_password.set(self.server_password.get())


class ExchangeSite(Site):

    ICON = ('icons.libreflow', 'exchange')

    server_url = flow.Param("")
    server_login = flow.Param("")
    server_password = flow.Param("").ui(editor='password')

    configuration = flow.Child(ConfigureExchangeSite)

    def compute_child_value(self, child_value):
        if child_value is self.configured:
            self.configured.set(
                (
                    self.server_url.get()
                    and self.server_login.get()
                    and self.server_password.get()
                )
            )


class ExchangeSites(SiteMap):
    
    ICON = ('icons.libreflow', 'exchange')

    @classmethod
    def mapped_type(cls):
        return ExchangeSite

    def mapped_names(self, page_num=0, page_size=None):
        return ["default_exchange"] + super(SiteMap, self).mapped_names(page_num, page_size)

    def _configure_child(self, child):
        if child.name() == "default_exchange":
            child.short_name.set("dftx")
            child.description.set("Default exchange site")
        else:
            super(ExchangeSites, self)._configure_child(child)

    def _get_mapped_item_type(self, mapped_name):
        if mapped_name == "default_exchange":
            return self.mapped_type()

        return super(SiteMap, self)._get_mapped_item_type(mapped_name)


class SyncSiteStatus(flow.Object):
    status = flow.Param("NotAvailable", StaticSiteSyncStatusChoices)

    def get_short_name(self):
        working_sites = self.root().project().get_working_sites()
        exchange_sites = self.root().project().get_exchange_sites()

        if working_sites.has_mapped_name(self.name()):
            site = working_sites[self.name()]
        else:
            site = exchange_sites[self.name()]

        return site.short_name.get()


class SyncMap(flow.DynamicMap):
    version = flow.Parent()

    @classmethod
    def mapped_type(cls):
        return SyncSiteStatus

    def mapped_names(self, page_num=0, page_size=None):
        working_sites = self.root().project().get_working_sites()
        exchange_sites = self.root().project().get_exchange_sites()
        
        return working_sites.mapped_names() + exchange_sites.mapped_names()

    def columns(self):
        return ['Name', 'Status']

    def _fill_row_cells(self, row, item):
        row['Status'] = item.status.get()
        row['Name'] = item.name()

        if item.name() == self.version.site.get():
            row['Name'] += " (S)"


class WorkingSiteChoiceValue(flow.values.ChoiceValue):

    _parent = flow.Parent()

    def choices(self):
        return self.root().project().get_working_sites().mapped_names()


class RequestRevisionsAs(flow.Action):

    pattern = flow.SessionParam("").watched().ui(
        placeholder="Revision oid pattern"
    )
    requesting_site_name = flow.Param("default", WorkingSiteChoiceValue).watched().ui(
        label="Requesting site"
    )
    requested_site_name = flow.Param("default", WorkingSiteChoiceValue).watched().ui(
        label="Site to query"
    )
    revision_oids = flow.SessionParam("").ui(
        editor="textarea",
        html=True,
        editable=False,
    )

    def allow_context(self, context):
        current_site = self.root().project().get_current_site()
        return context and current_site.request_files_from_anywhere.get()
    
    def _title(self):
        return "Request revisions"
    
    def child_value_changed(self, child_value):
        if child_value in (self.requesting_site_name, self.requested_site_name):
            msg = "<h2>%s</h2>" % self._title()
            if self.requested_site_name.get() == self.requesting_site_name.get():
                msg += (
                    "<font color=#D5000D>"
                    "Requested and requesting sites can't be the same."
                    "</font>"
                )

            self.message.set(msg)
        elif child_value is self.pattern:
            self._oids = self._get_oid(self.pattern.get())
            self.revision_oids.set("<br>".join(self._oids))
    
    def _get_oid(self, pattern_str):
        oids = []
        patterns = []
        
        for pattern in pattern_str.split(';'):
            patterns += self.resolve_pattern(pattern)
        
        for pattern in patterns:
            oids += self.glob(self.root().project().oid(), pattern, 0)
        
        return oids

    def get_buttons(self):
        self.requested_site_name.set(self.requested_site_name.choices()[0])
        self.revision_oids.set("")
        self._oids = []

        return ["Request", "Close"]
    
    def ls(self, root_oid):
        related_info, mapped_names = self.root().session().cmds.Flow.ls(root_oid)
        relation_oids = [rel_info[0] for rel_info in related_info]
        mapped_oids = ["%s/%s" % (root_oid, name) for name in mapped_names]
        
        return relation_oids + mapped_oids
    
    def get_last_publication(self, file_oid):
        o = self.root().get_object(file_oid)
        
        try:
            head = o.get_head_revision()
        except AttributeError:
            return None
        
        if not head:
            return None
        
        return head.name()
    
    def glob(self, root_oid, pattern, level):
        if level >= pattern.count("/") - 1:
            return [root_oid]

        matches = []
        level_pattern = "/".join(pattern.split("/")[:level + 3])

        if level_pattern.endswith("[last]"):
            file_oid = self.root().session().cmds.Flow.resolve_path(root_oid + "/../..")
            head_name = self.get_last_publication(file_oid)

            if not head_name:
                return []
            
            pattern = pattern.replace("[last]", head_name)
            level_pattern = level_pattern.replace("[last]", head_name)
        
        for oid in self.ls(root_oid):
            if fnmatch.fnmatch(oid, level_pattern):
                matches += self.glob(oid, pattern, level + 1)
        
        return matches
    
    def resolve_pattern(self, pattern_oid):
        '''
        Returns a list of patterns which correspond to all substitution combinations of `pattern_oid`.
        Substitute string are specified in `pattern_oid` between brackets and separated with comas (`{s0, s1, ...}`).
        '''
        match = re.search(r'{[^{}]+}', pattern_oid)

        if not match:
            return [pattern_oid]

        substitutes = match.group()[1:-1].split(',')
        substitutes = [sub.replace(' ', '') for sub in substitutes]

        sub_oids = [pattern_oid.replace(match.group(), sub, 1) for sub in substitutes]
        oids = []

        for sub_oid in sub_oids:
            oids += self.resolve_pattern(sub_oid)
        
        return oids

    
    def run(self, button):
        if button == "Close":
            return
        
        if not self._oids:
            self._oids = self._get_oid(self.pattern.get())

        objects = [self.root().get_object(oid) for oid in self._oids]
        processed_oids = []
        
        for o in objects:
            oid = o.oid()

            if hasattr(o, 'request_as') and o.ready_for_sync.get():
                requested_site_name = self.requested_site_name.get()
                requesting_site_name = self.requesting_site_name.get()

                if not requesting_site_name in o.request_as.requesting_site_name.choices():
                    oid += f" <font color='red'>Available on {requesting_site_name}</font>"
                elif not requested_site_name in o.request_as.requested_site_name.choices():
                    oid += f" <font color='red'>Not available on {requested_site_name}</font>"
                else:
                    o.request_as.requested_site_name.set(requested_site_name)
                    o.request_as.requesting_site_name.set(requesting_site_name)
                    o.request_as.run(None)
                    oid += " <font color='green'>OK</font>"
            else:
                if not o.ready_for_sync.get():
                    msg = "Revision not ready for sync"
                else:
                    msg = "Not a file revision"
                
                oid += " <font color='red'>%s</font>" % msg
            
            processed_oids.append(oid)
        
        self.revision_oids.set("<br>".join(processed_oids))

        return self.get_result(close=False)
