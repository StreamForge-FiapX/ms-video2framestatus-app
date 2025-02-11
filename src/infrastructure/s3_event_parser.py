class S3EventParser:
    STAGE_MAPPING = {
        "video-uploaded": "INICIADO",
        "video-chunks": "EM PROGRESSO",
        "frames-chunks-video": "FINALIZADO"
    }

    def parse(self, event):
        sqs_record = event['Records'][0]
        sns_message_body = json.loads(sqs_record['body'])
        sns_message = json.loads(sns_message_body['Message'])
        record = sns_message['Records'][0]

        bucket_name = record['s3']['bucket']['name']
        object_key = unquote(record['s3']['object']['key'])
        status = self.STAGE_MAPPING.get(bucket_name, "DESCONHECIDO")

        key_parts = object_key.split('/')
        if len(key_parts) < 2:
            raise ValueError("Formato inválido da key do S3")

        return {
            "user": key_parts[0],
            "upload_date": key_parts[1],
            "video_title": key_parts[2] if len(key_parts) >= 3 else "DESCONHECIDO",
            "s3_uri": f"s3://{bucket_name}/{object_key}",
            "status": status
        }
