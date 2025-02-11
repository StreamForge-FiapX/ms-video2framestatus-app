from domain.repositories import RedisRepositoryInterface


class ProcessEventUseCase:
    def __init__(self, redis_repo: RedisRepositoryInterface, s3_parser):
        self.redis_repo = redis_repo
        self.s3_parser = s3_parser

    def execute(self, event):
        s3_data = self.s3_parser.parse(event)
        redis_key = f"video-status:{s3_data['user']}:{s3_data['upload_date']}:{s3_data['video_title']}"

        redis_data = {
            "video_title": s3_data["video_title"],
            "s3_uri": s3_data["s3_uri"],
            "status": s3_data["status"],
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }

        self.redis_repo.save(redis_key, redis_data)
        return f"Status atualizado para {s3_data['status']} no Redis para {s3_data['video_title']}"
