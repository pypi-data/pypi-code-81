from aws_cdk import (
    core, 
    aws_ecr as _ecr
)

class ECR(_ecr.Repository):
    '''
    Subclass of aws_ecr.Repository. 
    It creates a ECR repository with the some default settings that cannot be overriden:
        image_scan_on_push (Boolean) - set to True.
        repository_name ( String ) - set to be the same as id
        lifecycle_rules ( List[LifecycleRule] )
    '''
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:

        # image_tag_mutability = _ecr.TagMutability.IMMUTABLE
        # TODO: 
        # eventhough class TagMutability is documented here:
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ecr/TagMutability.html#aws_cdk.aws_ecr.TagMutability
        # it is not in the aws_ecr package. 
        # issue: https://github.com/aws/aws-cdk/issues/4640

        # to add default lifecycle rules, append to list
        lifecycle_rules = []

        super().__init__(scope, id, 
            repository_name=id, 
            image_scan_on_push=True,
            **kwargs)
    