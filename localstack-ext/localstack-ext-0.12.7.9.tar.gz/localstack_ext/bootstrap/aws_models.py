from localstack.utils.aws import aws_models
lFcik=super
lFciK=None
lFcih=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  lFcik(LambdaLayer,self).__init__(arn)
  self.cwd=lFciK
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.lFcih.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(RDSDatabase,self).__init__(lFcih,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(RDSCluster,self).__init__(lFcih,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(AppSyncAPI,self).__init__(lFcih,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(AmplifyApp,self).__init__(lFcih,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(ElastiCacheCluster,self).__init__(lFcih,env=env)
class TransferServer(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(TransferServer,self).__init__(lFcih,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(CloudFrontDistribution,self).__init__(lFcih,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,lFcih,env=lFciK):
  lFcik(CodeCommitRepository,self).__init__(lFcih,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
