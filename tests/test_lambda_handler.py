import os
import json
import unittest
from unittest.mock import patch, MagicMock
from lambda_handler import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    @patch('lambda_handler.RedisRepository')
    @patch('lambda_handler.S3EventParser')
    @patch('lambda_handler.ProcessEventUseCase')
    def test_lambda_handler(self, MockUseCase, MockS3Parser, MockRedisRepo):
        event = {"Records": [{"body": '{"Message": "{\\"Records\\": [{\\"s3\\": {\\"bucket\\": {\\"name\\": \\"video-uploaded\\"}, \\"object\\": {\\"key\\": \\"user/upload/filename\\"}}}]}"}'}]}
        context = {}

        mock_use_case = MagicMock()
        mock_use_case.execute.return_value = "Status atualizado"
        MockUseCase.return_value = mock_use_case

        mock_redis_repo = MagicMock()
        MockRedisRepo.return_value = mock_redis_repo

        mock_s3_parser = MagicMock()
        MockS3Parser.return_value = mock_s3_parser

        response = lambda_handler(event, context)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("body", response)
        self.assertEqual(response["body"], "Status atualizado")

if __name__ == '__main__':
    unittest.main()
