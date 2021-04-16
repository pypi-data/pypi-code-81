from localstack.utils.aws import aws_models
wqNkC=super
wqNkW=None
wqNkJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  wqNkC(LambdaLayer,self).__init__(arn)
  self.cwd=wqNkW
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.wqNkJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(RDSDatabase,self).__init__(wqNkJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(RDSCluster,self).__init__(wqNkJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(AppSyncAPI,self).__init__(wqNkJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(AmplifyApp,self).__init__(wqNkJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(ElastiCacheCluster,self).__init__(wqNkJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(TransferServer,self).__init__(wqNkJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(CloudFrontDistribution,self).__init__(wqNkJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,wqNkJ,env=wqNkW):
  wqNkC(CodeCommitRepository,self).__init__(wqNkJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
