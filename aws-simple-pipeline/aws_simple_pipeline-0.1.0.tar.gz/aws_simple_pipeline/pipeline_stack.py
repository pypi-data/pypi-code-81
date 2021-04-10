"""The class for managing your simple AWS CDK pipeline

The class requires the follow properties:
    'id' (str): the name of project used for the prefix of the stack name
    'stage' (str): the name of the environment, default is empty
    'github_owner' (str): the github owner
    'github_repo' (str): the github repository name
    'github_branch' (str): the github repository branch
    'github_token' (obj): AWS object with reference like Secrets Manager
    'notify_emails' (list): list of emails to notify
    'policies' (list): list of policies name to add 
    'buildspec_path' (str): path of buildspec file, default: buildspec.yml
    'manual_approval_exists' (bool): if True, then there will be a manual approval stage

All properties are mandatory, except the last one that it has a default value of False, and the stage property.
Here's an example:

    >>> from aws_cdk import core
    >>> from aws_simple_pipeline.pipeline_stack import PipelineStack
    >>> app = core.App()
    >>> PipelineStack(app,
    >>>     id="aws-simple-pipeline",
    >>>     stage="sample",
    >>>     github_owner="bilardi",
    >>>     github_repo="aws-simple-pipeline",
    >>>     github_branch="master",
    >>>     github_token=core.SecretValue.secrets_manager("/github/token",json_field='github-token'),
    >>>     notify_emails=[ "your@email.net" ],
    >>>     policies=[ "AdministratorAccess" ], # avoid in production
    >>>     buildspec_path="buildspec.yml",
    >>>     manual_approval_exists=True
    >>> )
    >>> app.synth()

# license MIT
# support https://github.com/bilardi/aws-simple-pipeline/issues
"""
from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_s3 as s3, aws_iam as iam)

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *, stage: str='', github_owner: str=None, github_repo: str=None, github_branch: str=None, github_token: str=None, notify_emails: list=None, policies: list=None, buildspec_path: str='buildspec.yml', manual_approval_exists: bool=False, **kwargs) -> None:
        """
        deploys all AWS resources for your pipeline
            Resources:
                AWS::IAM::Role with your policies
                AWS::S3::Bucket for your artifacts
                AWS::CodeBuild::Project that it loads your buildspec.yml on LinuxBuildImage.STANDARD_4_0
                AWS::CodePipeline::Webhook for triggering your pipeline to start every time github-push occurs
                AWS::CodePipeline::Pipeline with the stages named Source, Staging, Manual Approval and Production
        """
        super().__init__(scope, id, **kwargs)

        if scope.node.try_get_context("stage"):
            stage = scope.node.try_get_context("stage")
        if stage:
            stage = '-' + stage

        role = iam.Role(self, "role", assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"))
        for policy in policies:
            role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(policy))

        artifact_bucket = s3.Bucket(
            self, 'BuildArtifactsBucket',
            removal_policy=core.RemovalPolicy.DESTROY,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            versioned=False,
        )

        project = codebuild.PipelineProject(
            self, "Project",
            project_name=id,
            build_spec=codebuild.BuildSpec.from_source_filename(buildspec_path),
            cache=codebuild.Cache.bucket(artifact_bucket, prefix='codebuild-cache'),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_4_0
            ),
            role=role
        )

        source_output = codepipeline.Artifact()
        staging_output = codepipeline.Artifact()
        production_output = codepipeline.Artifact()

        stages = [
            codepipeline.StageProps(
                stage_name="Source",
                actions=[
                    codepipeline_actions.GitHubSourceAction(
                        action_name="GitHub",
                        owner=github_owner,
                        repo=github_repo,
                        branch=github_branch,
                        oauth_token=github_token,
                        output=source_output
                    )
                ]
            ),
            codepipeline.StageProps(
                stage_name="Staging",
                actions=[
                    codepipeline_actions.CodeBuildAction(
                        action_name="StagingDeploy",
                        project=project,
                        input=source_output,
                        outputs=[staging_output],
                        environment_variables={
                            "ENV": codebuild.BuildEnvironmentVariable(value="staging" + stage)
                        }
                    )
                ]
            ),
            codepipeline.StageProps(
                stage_name="ManualApproval",
                actions=[
                    codepipeline_actions.ManualApprovalAction(
                        action_name="ManualApproval",
                        notify_emails=notify_emails
                    )
                ]
            ),
            codepipeline.StageProps(
                stage_name="Production",
                actions=[
                    codepipeline_actions.CodeBuildAction(
                        action_name="ProductionDeploy",
                        project=project,
                        input=source_output,
                        outputs=[production_output],
                        environment_variables={
                            "ENV": codebuild.BuildEnvironmentVariable(value="production" + stage)
                        }
                    )
                ]
            )
        ]
        if manual_approval_exists == False:
            del stages[2]

        codepipeline.Pipeline(
            self, "Pipeline",
            stages=stages
        )
