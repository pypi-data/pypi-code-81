from aws_cdk import (
  core,
  aws_iam as _iam,
  aws_codebuild as _codebuild,
  aws_codepipeline_actions as _codepipeline_actions
)

class DockerBuildAction(_codepipeline_actions.CodeBuildAction):
    '''
    Subclass of CodeBuildAction. 
    It creates a CodeBuild project that can build docker images and push images to ECR

    Parameters are the same as the parent class: 
    https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_codepipeline_actions/CodeBuildAction.html
    except the following Changes:
      scope (Construct) - Added as a required parameter.
      project (Optional [IProject]) - this parameter receives a default value. Default: an automatically created CodeBuild project that has privileged set to True.
    '''
    def __init__(self, scope: core.Construct, **kwargs):
      if 'project' not in kwargs:
        # create codebuild project
        default_project = _codebuild.PipelineProject(scope, 'DockerCodeBuild', environment=_codebuild.BuildEnvironment(privileged=True))
        
        # add policy statement that grants ECR access to the codebuild project Role
        ecr_policy = _iam.PolicyStatement(
          actions=['ecr:*'],
          resources=['*']
        )
        default_project.add_to_role_policy(ecr_policy)

        kwargs['project'] = default_project
      super().__init__(**kwargs)

