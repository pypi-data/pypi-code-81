from localstack.utils.aws import aws_models
Ksndh=super
KsndS=None
KsndJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Ksndh(LambdaLayer,self).__init__(arn)
  self.cwd=KsndS
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KsndJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(RDSDatabase,self).__init__(KsndJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(RDSCluster,self).__init__(KsndJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(AppSyncAPI,self).__init__(KsndJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(AmplifyApp,self).__init__(KsndJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(ElastiCacheCluster,self).__init__(KsndJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(TransferServer,self).__init__(KsndJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(CloudFrontDistribution,self).__init__(KsndJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KsndJ,env=KsndS):
  Ksndh(CodeCommitRepository,self).__init__(KsndJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
