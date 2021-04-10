from localstack.utils.aws import aws_models
nYtOw=super
nYtOv=None
nYtOU=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nYtOw(LambdaLayer,self).__init__(arn)
  self.cwd=nYtOv
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.nYtOU.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(RDSDatabase,self).__init__(nYtOU,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(RDSCluster,self).__init__(nYtOU,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(AppSyncAPI,self).__init__(nYtOU,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(AmplifyApp,self).__init__(nYtOU,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(ElastiCacheCluster,self).__init__(nYtOU,env=env)
class TransferServer(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(TransferServer,self).__init__(nYtOU,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(CloudFrontDistribution,self).__init__(nYtOU,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,nYtOU,env=nYtOv):
  nYtOw(CodeCommitRepository,self).__init__(nYtOU,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
