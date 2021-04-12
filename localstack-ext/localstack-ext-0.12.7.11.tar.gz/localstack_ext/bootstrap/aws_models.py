from localstack.utils.aws import aws_models
RWXPx=super
RWXPQ=None
RWXPs=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RWXPx(LambdaLayer,self).__init__(arn)
  self.cwd=RWXPQ
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.RWXPs.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(RDSDatabase,self).__init__(RWXPs,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(RDSCluster,self).__init__(RWXPs,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(AppSyncAPI,self).__init__(RWXPs,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(AmplifyApp,self).__init__(RWXPs,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(ElastiCacheCluster,self).__init__(RWXPs,env=env)
class TransferServer(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(TransferServer,self).__init__(RWXPs,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(CloudFrontDistribution,self).__init__(RWXPs,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,RWXPs,env=RWXPQ):
  RWXPx(CodeCommitRepository,self).__init__(RWXPs,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
