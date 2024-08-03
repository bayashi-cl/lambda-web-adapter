from typing import Any

from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel


class Request(BaseModel):
    question: str


class Response(BaseModel):
    answer: str


@event_parser()
def handler(event: Request, context: LambdaContext) -> dict[str, Any]:
    return Response(answer=event.question + "!!!").model_dump()
