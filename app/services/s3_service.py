# app/services/s3_service.py
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from app.config import settings
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class S3Service:
    """AWS S3 파일 업로드 및 다운로드 유틸리티"""

    def __init__(self):
        # ✅ 환경변수 기반으로 S3 클라이언트 설정
        if not all([settings.aws_access_key_id, settings.aws_secret_access_key, settings.aws_region]):
            raise ValueError("AWS 자격 증명이 누락되었습니다. (.env 파일 확인 필요)")
        
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.bucket_name = settings.aws_s3_bucket
        logger.info(f"🪣 Connected to S3 bucket: {self.bucket_name}")

    # -------------------------------------------------
    # 📤 파일 업로드
    # -------------------------------------------------
    def upload_file(self, file_path: str, s3_key: Optional[str] = None) -> str:
        """로컬 파일을 S3에 업로드"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

        s3_key = s3_key or file_path.name

        try:
            self.s3.upload_file(
                Filename=str(file_path),
                Bucket=self.bucket_name,
                Key=s3_key,
                ExtraArgs={"ACL": "private"}  # 권한: private (필요 시 public-read)
            )
            logger.info(f"✅ 업로드 완료: {file_path} → s3://{self.bucket_name}/{s3_key}")
            return f"s3://{self.bucket_name}/{s3_key}"
        except NoCredentialsError:
            logger.error("❌ AWS 자격 증명 오류 — .env 파일 또는 IAM 설정을 확인하세요.")
            raise
        except ClientError as e:
            logger.error(f"❌ 업로드 실패: {e}")
            raise

    # -------------------------------------------------
    # 📥 파일 다운로드
    # -------------------------------------------------
    def download_file(self, s3_key: str, local_path: str) -> Path:
        """S3 파일을 로컬로 다운로드"""
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.s3.download_file(self.bucket_name, s3_key, str(local_path))
            logger.info(f"📥 다운로드 완료: s3://{self.bucket_name}/{s3_key} → {local_path}")
            return local_path
        except ClientError as e:
            logger.error(f"❌ 다운로드 실패: {e}")
            raise

    # -------------------------------------------------
    # ❌ 파일 삭제
    # -------------------------------------------------
    def delete_file(self, s3_key: str) -> bool:
        """S3 파일 삭제"""
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"🗑️ 삭제 완료: s3://{self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            logger.error(f"❌ 삭제 실패: {e}")
            return False

    # -------------------------------------------------
    # 🔗 presigned URL 생성
    # -------------------------------------------------
    def generate_presigned_url(self, s3_key: str, expires_in: int = 3600) -> str:
        """임시 다운로드 URL 생성 (기본 만료 1시간)"""
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_key},
                ExpiresIn=expires_in
            )
            logger.info(f"🔗 Presigned URL 생성: {url}")
            return url
        except ClientError as e:
            logger.error(f"❌ URL 생성 실패: {e}")
            raise


# ✅ 싱글톤 인스턴스 생성 (FastAPI에서 바로 사용 가능)
s3_service = S3Service()
