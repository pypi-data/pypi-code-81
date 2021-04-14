from eo_lib.model.core.models import ApplicationReference
from eo_lib.service.core.service import ApplicationReferenceService, ConfigurationService, ApplicationService, ApplicationTypeService
from eo_lib.application.abstract_application import AbstractApplication


class ApplicationApplicationType(AbstractApplication):
    
    def __init__(self):
        super().__init__(ApplicationTypeService())

class ApplicationApplication(AbstractApplication):
    
    def __init__(self):
        super().__init__(ApplicationService())

class ApplicationConfiguration(AbstractApplication):
    
    def __init__(self):
        super().__init__(ConfigurationService())
    
    def retrive_by_organization_and_application(self, organization, application):
        return self.service.retrive_by_organization_and_application(organization, application)
    

class ApplicationApplicationReference(AbstractApplication):
    
    def __init__(self):
        super().__init__(ApplicationReferenceService())
        
 