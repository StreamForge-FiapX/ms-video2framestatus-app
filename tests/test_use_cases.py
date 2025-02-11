import unittest
from unittest.mock import MagicMock
from process_event_use_case import ProcessEventUseCase

class TestProcessEventUseCase(unittest.TestCase):
    def test_execute(self):
        mock_redis_repo = MagicMock()
        mock_s3_parser = MagicMock()
        mock_s3_parser.parse.return_value = {
            "user": "user",
            "upload_date": "2025-02-10",
            "video_title": "video_title",
            "s3_uri": "s3://bucket/key",
            "status": "INICIADO"
        }

        use_case = ProcessEventUseCase(mock_redis_repo, mock_s3_parser)
        response = use_case.execute({"Records": []})

        self.assertIn("Status atualizado", response)

if __name__ == '__main__':
    unittest.main()
