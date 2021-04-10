from localstack.utils.aws import aws_models
BLanC=super
BLanN=None
BLanA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  BLanC(LambdaLayer,self).__init__(arn)
  self.cwd=BLanN
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.BLanA.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(RDSDatabase,self).__init__(BLanA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(RDSCluster,self).__init__(BLanA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(AppSyncAPI,self).__init__(BLanA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(AmplifyApp,self).__init__(BLanA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(ElastiCacheCluster,self).__init__(BLanA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(TransferServer,self).__init__(BLanA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(CloudFrontDistribution,self).__init__(BLanA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,BLanA,env=BLanN):
  BLanC(CodeCommitRepository,self).__init__(BLanA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
