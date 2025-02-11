import unittest
from unittest.mock import MagicMock
from s3_event_parser import S3EventParser

class TestS3EventParser(unittest.TestCase):
    def test_parse_valid_event(self):
        event = {
            "Records": [{
                "body": '{"Message": "{\\"Records\\": [{\\"s3\\": {\\"bucket\\": {\\"name\\": \\"video-uploaded\\"}, \\"object\\": {\\"key\\": \\"user/upload/video_title\\"}}}]}"}'
            }]
        }
        s3_parser = S3EventParser()
        result = s3_parser.parse(event)
        self.assertEqual(result["user"], "user")
        self.assertEqual(result["video_title"], "video_title")
        self.assertEqual(result["status"], "INICIADO")

    def test_parse_invalid_event(self):
        event = {
            "Records": [{
                "body": '{"Message": "{\\"Records\\": [{\\"s3\\": {\\"bucket\\": {\\"name\\": \\"unknown\\"}, \\"object\\": {\\"key\\": \\"user/upload/video_title\\"}}}]}"}'
            }]
        }
        s3_parser = S3EventParser()
        result = s3_parser.parse(event)
        self.assertEqual(result["status"], "DESCONHECIDO")

if __name__ == '__main__':
    unittest.main()
