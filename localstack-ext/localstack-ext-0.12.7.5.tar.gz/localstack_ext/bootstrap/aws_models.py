from localstack.utils.aws import aws_models
eirDc=super
eirDV=None
eirDg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  eirDc(LambdaLayer,self).__init__(arn)
  self.cwd=eirDV
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.eirDg.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(RDSDatabase,self).__init__(eirDg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(RDSCluster,self).__init__(eirDg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(AppSyncAPI,self).__init__(eirDg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(AmplifyApp,self).__init__(eirDg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(ElastiCacheCluster,self).__init__(eirDg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(TransferServer,self).__init__(eirDg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(CloudFrontDistribution,self).__init__(eirDg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,eirDg,env=eirDV):
  eirDc(CodeCommitRepository,self).__init__(eirDg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
