from localstack.utils.aws import aws_models
lXarY=super
lXarq=None
lXarJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lXarY(LambdaLayer,self).__init__(arn)
  self.cwd=lXarq
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lXarJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(RDSDatabase,self).__init__(lXarJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(RDSCluster,self).__init__(lXarJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(AppSyncAPI,self).__init__(lXarJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(AmplifyApp,self).__init__(lXarJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(ElastiCacheCluster,self).__init__(lXarJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(TransferServer,self).__init__(lXarJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(CloudFrontDistribution,self).__init__(lXarJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lXarJ,env=lXarq):
  lXarY(CodeCommitRepository,self).__init__(lXarJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
