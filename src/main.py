import os
import json
import logging
from datetime import datetime
from urllib.parse import unquote

from domain.use_cases import ProcessEventUseCase
from infrastructure.s3_event_parser import S3EventParser
from infrastructure.redis_repository import RedisRepository

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recebido: {json.dumps(event, indent=2)}")

        redis_host = os.environ.get("REDIS_HOST")
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        redis_password = os.environ.get("REDIS_PASSWORD", None)

        redis_repo = RedisRepository(redis_host, redis_port, redis_password)
        s3_parser = S3EventParser()
        use_case = ProcessEventUseCase(redis_repo, s3_parser)

        response = use_case.execute(event)
        return {"statusCode": 200, "body": response}

    except Exception as e:
        logger.error(f"Erro no processamento do evento: {e}")
        return {"statusCode": 500, "body": f"Erro no processamento: {str(e)}"}
