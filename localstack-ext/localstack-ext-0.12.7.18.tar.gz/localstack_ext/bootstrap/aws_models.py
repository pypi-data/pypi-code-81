from localstack.utils.aws import aws_models
dRWnw=super
dRWnz=None
dRWnV=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dRWnw(LambdaLayer,self).__init__(arn)
  self.cwd=dRWnz
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dRWnV.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(RDSDatabase,self).__init__(dRWnV,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(RDSCluster,self).__init__(dRWnV,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(AppSyncAPI,self).__init__(dRWnV,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(AmplifyApp,self).__init__(dRWnV,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(ElastiCacheCluster,self).__init__(dRWnV,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(TransferServer,self).__init__(dRWnV,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(CloudFrontDistribution,self).__init__(dRWnV,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dRWnV,env=dRWnz):
  dRWnw(CodeCommitRepository,self).__init__(dRWnV,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
