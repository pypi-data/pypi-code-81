from localstack.utils.aws import aws_models
FiuVx=super
FiuVw=None
FiuVJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  FiuVx(LambdaLayer,self).__init__(arn)
  self.cwd=FiuVw
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.FiuVJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(RDSDatabase,self).__init__(FiuVJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(RDSCluster,self).__init__(FiuVJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(AppSyncAPI,self).__init__(FiuVJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(AmplifyApp,self).__init__(FiuVJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(ElastiCacheCluster,self).__init__(FiuVJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(TransferServer,self).__init__(FiuVJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(CloudFrontDistribution,self).__init__(FiuVJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,FiuVJ,env=FiuVw):
  FiuVx(CodeCommitRepository,self).__init__(FiuVJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
