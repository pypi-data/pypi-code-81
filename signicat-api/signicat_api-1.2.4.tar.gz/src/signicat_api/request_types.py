import json

SWISHFUND_NO_REPLY_EMAIL = 'no-reply@swishfund.nl'

class RequestType:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)


class Document:

    def __init__(self, id: str, action: str, description: str, document_ref: str, source: str):
        self.source = source
        self.id = id
        self.documentRef = document_ref
        self.description = description
        self.action = action


class SignatureMethod:
    def __init__(self, handwritten: bool, name: str, type: str):
        self.type = type
        self.name = name
        self.handwritten = handwritten

    @staticmethod
    def sms(handwritten: bool = True):
        return SignatureMethod(handwritten, 'scid-sms', 'AUTHENTICATION_BASED')

    @staticmethod
    def idin(handwritten: bool = True):
        return SignatureMethod(handwritten, 'idin', 'AUTHENTICATION_BASED')


class NotificationSchedule:
    def __init__(self, trigger_status: str):
        self.triggerStatus = trigger_status


class Notification:
    def __init__(self, id: str, header: str, message: str, recipient: str, schedule: [NotificationSchedule], sender: str, type: str):
        self.type = type
        self.sender = sender
        self.schedule = schedule
        self.recipient = recipient
        self.message = message
        self.header = header
        self.id = id

    @staticmethod
    def created(task_notification_id: str, to_email: str):
        """
        Default created notification to reduces boilerplate code
        """
        return Notification(task_notification_id,
                                     'Signicat - document ready to be signed',
                                     'Dear,\n\nA document is ready to be signed at the following link:\n\n${signCodeUrl}\n\nRegards,\nSignicat',
                                     to_email,
                                     [NotificationSchedule('CREATED')],
                                     SWISHFUND_NO_REPLY_EMAIL,
                                     'EMAIL')

    @staticmethod
    def completed(task_notification_id: str, to_email: str):
        """
        Default completed notification to reduces boilerplate code
        """
        return Notification(task_notification_id,
                                     'Signicat - document signed successfully',
                                     'Dear,\n\nYou have successfully signed the document\n\nRegards,\nSignicat',
                                     to_email,
                                     [NotificationSchedule('COMPLETED')],
                                     SWISHFUND_NO_REPLY_EMAIL,
                                     'EMAIL')

    @staticmethod
    def pades(task_notification_id: str, to_email: str):
        """
        Default pades notification to reduces boilerplate code
        """
        return Notification(task_notification_id,
                     'Signicat - pades generated successfully',
                     'Dear,\n\nThe pades has been generated successfully\n\nRegards,\nSignicat',
                     to_email,
                     [NotificationSchedule('COMPLETED')],
                     SWISHFUND_NO_REPLY_EMAIL,
                     'EMAIL')


class TaskAuthentication:
    def __init__(self, methods: [str]):
        self.methods = methods

    @staticmethod
    def sms():
        return TaskAuthentication(['scid-sms'])


class Task:
    def __init__(self, id: str, configuration: str, documents: [Document], signature_methods: [SignatureMethod], on_task_complete: str, notifications: [Notification], authentication: TaskAuthentication = None):
        self.id = id
        self.configuration = configuration
        self.documents = documents
        self.signatureMethods = signature_methods
        self.notifications = notifications
        self.onTaskComplete = on_task_complete
        self.authentication = authentication


class PackagingTaskDocuments:
    def __init__(self, task_id: str, document_ids: [str]):
        self.documentIds = document_ids
        self.taskId = task_id


class PackagingTask:
    def __init__(self, id: str, send_to_archive: bool, method: str, notifications: [Notification], documents: [PackagingTaskDocuments]):
        self.documents = documents
        self.notifications = notifications
        self.method = method
        self.sendToArchive = send_to_archive
        self.id = id


class SignOrder(RequestType):
    def __init__(self, client_reference: str or None, tasks: [Task], packaging_tasks: [PackagingTask]):
        self.clientReference = client_reference
        self.tasks = tasks
        self.packagingTasks = packaging_tasks