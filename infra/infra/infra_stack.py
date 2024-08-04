import textwrap

from aws_cdk import (
    BundlingOptions,
    DockerImage,
    RemovalPolicy,
    Stack,
    aws_apigateway,
    aws_lambda,
    aws_logs,
)
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

        runtime: aws_lambda.Runtime = aws_lambda.Runtime.PYTHON_3_12
        python_deps = aws_lambda.LayerVersion(
            self,
            "PythonDepsLayer",
            code=aws_lambda.Code.from_asset(
                "../api",
                bundling=BundlingOptions(
                    image=DockerImage.from_build(
                        "docker",
                        build_args={"IMAGE": runtime.bundling_image.image},
                        file="Dockerfile.poetry",
                    ),
                    command=[
                        "bash",
                        "-c",
                        textwrap.dedent(
                            """\
                            set -eux
                            poetry export --without-hashes --format constraints.txt --output /tmp/constraints.txt
                            pip install . --ignore-installed --constraint /tmp/constraints.txt --prefix /asset-output/python
                            """
                            # Note:
                            # The following command does not work well due to symlink.
                            # ```poetry bundle venv --without dev /asset-output/python```
                            # See https://github.com/aws/aws-cdk/issues/9251
                        ),
                    ],
                ),
            ),
        )

        api = aws_lambda.Function(
            self,
            "ApiFunction",
            code=aws_lambda.Code.from_asset("../api/lambda-scripts"),
            layers=[
                python_deps,
                aws_lambda.LayerVersion.from_layer_version_arn(
                    self,
                    "WebAppAdaptorLayer",
                    f"arn:aws:lambda:{self.region}:753240598075:layer:LambdaAdapterLayerX86:23",
                ),
            ],
            runtime=runtime,
            environment={
                "AWS_LAMBDA_EXEC_WRAPPER": "/opt/bootstrap",
                "AWS_LWA_PORT": "8000",
                "AWS_LWA_READINESS_CHECK_PATH": "/check",
                "APP_LAMBDA_ARN": app.function_arn,
            },
            handler="run.sh",
            log_group=aws_logs.LogGroup(
                self,
                "ApiLogGroup",
                removal_policy=RemovalPolicy.DESTROY,
            ),
            logging_format=aws_lambda.LoggingFormat.JSON,
            application_log_level_v2=aws_lambda.ApplicationLogLevel.INFO,
        )
        app.grant_invoke(api)

        aws_apigateway.LambdaRestApi(self, "ApiGw", handler=api)
