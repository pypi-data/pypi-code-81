from localstack.utils.aws import aws_models
yIufh=super
yIufk=None
yIufq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yIufh(LambdaLayer,self).__init__(arn)
  self.cwd=yIufk
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.yIufq.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(RDSDatabase,self).__init__(yIufq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(RDSCluster,self).__init__(yIufq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(AppSyncAPI,self).__init__(yIufq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(AmplifyApp,self).__init__(yIufq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(ElastiCacheCluster,self).__init__(yIufq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(TransferServer,self).__init__(yIufq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(CloudFrontDistribution,self).__init__(yIufq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,yIufq,env=yIufk):
  yIufh(CodeCommitRepository,self).__init__(yIufq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
