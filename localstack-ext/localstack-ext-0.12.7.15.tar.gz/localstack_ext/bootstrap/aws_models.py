from localstack.utils.aws import aws_models
oxKMr=super
oxKMd=None
oxKMn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  oxKMr(LambdaLayer,self).__init__(arn)
  self.cwd=oxKMd
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.oxKMn.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(RDSDatabase,self).__init__(oxKMn,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(RDSCluster,self).__init__(oxKMn,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(AppSyncAPI,self).__init__(oxKMn,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(AmplifyApp,self).__init__(oxKMn,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(ElastiCacheCluster,self).__init__(oxKMn,env=env)
class TransferServer(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(TransferServer,self).__init__(oxKMn,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(CloudFrontDistribution,self).__init__(oxKMn,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,oxKMn,env=oxKMd):
  oxKMr(CodeCommitRepository,self).__init__(oxKMn,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
