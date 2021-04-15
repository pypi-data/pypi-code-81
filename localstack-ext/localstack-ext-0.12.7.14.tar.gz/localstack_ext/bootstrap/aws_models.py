from localstack.utils.aws import aws_models
zcTtC=super
zcTta=None
zcTtM=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  zcTtC(LambdaLayer,self).__init__(arn)
  self.cwd=zcTta
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.zcTtM.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(RDSDatabase,self).__init__(zcTtM,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(RDSCluster,self).__init__(zcTtM,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(AppSyncAPI,self).__init__(zcTtM,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(AmplifyApp,self).__init__(zcTtM,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(ElastiCacheCluster,self).__init__(zcTtM,env=env)
class TransferServer(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(TransferServer,self).__init__(zcTtM,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(CloudFrontDistribution,self).__init__(zcTtM,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,zcTtM,env=zcTta):
  zcTtC(CodeCommitRepository,self).__init__(zcTtM,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
