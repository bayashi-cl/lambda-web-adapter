from aws_cdk import RemovalPolicy, Stack, aws_apigateway, aws_lambda, aws_logs
from constructs import Construct


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        app = aws_lambda.DockerImageFunction(
            self,
            "AppFunction",
            code=aws_lambda.DockerImageCode.from_image_asset("../app"),
            log_group=aws_logs.LogGroup(
                self,
                "AppLogGroup",
                removal_policy=RemovalPolicy.DESTROY,
            ),
            logging_format=aws_lambda.LoggingFormat.JSON,
            application_log_level_v2=aws_lambda.ApplicationLogLevel.INFO,
        )

        aws_apigateway.LambdaRestApi(self, "ApiGw", handler=app)
