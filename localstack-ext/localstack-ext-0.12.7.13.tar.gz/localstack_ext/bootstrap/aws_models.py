from localstack.utils.aws import aws_models
SrYsV=super
SrYsL=None
SrYsv=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  SrYsV(LambdaLayer,self).__init__(arn)
  self.cwd=SrYsL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.SrYsv.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(RDSDatabase,self).__init__(SrYsv,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(RDSCluster,self).__init__(SrYsv,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(AppSyncAPI,self).__init__(SrYsv,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(AmplifyApp,self).__init__(SrYsv,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(ElastiCacheCluster,self).__init__(SrYsv,env=env)
class TransferServer(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(TransferServer,self).__init__(SrYsv,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(CloudFrontDistribution,self).__init__(SrYsv,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,SrYsv,env=SrYsL):
  SrYsV(CodeCommitRepository,self).__init__(SrYsv,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
