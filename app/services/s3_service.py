# app/services/s3_service.py
import boto3
import logging
import time
from botocore.exceptions import NoCredentialsError, ClientError, EndpointConnectionError
from app.config import settings
from typing import Optional
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger("soulstay.s3")

@lru_cache(maxsize=1)
def get_s3_client():
    """S3 클라이언트 캐싱 (재사용 성능 향상)"""
    return boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )

class S3Service:
    """AWS S3 파일 업로드 및 다운로드 안정화 버전"""

    def __init__(self):
        try:
            self.s3 = get_s3_client()
            self.bucket_name = settings.aws_s3_bucket_name
            self.health_check()  # ✅ 연결 유효성 검사
            logger.info(f"🪣 Connected to S3 bucket: {self.bucket_name}")
        except Exception as e:
            logger.exception(f"S3 초기화 실패: {e}")
            raise

    def health_check(self) -> bool:
        """S3 연결 테스트"""
        try:
            self.s3.head_bucket(Bucket=settings.aws_s3_bucket_name)
            return True
        except Exception as e:
            logger.error(f"🚨 S3 연결 확인 실패: {e}")
            return False

    def _retry(self, func, *args, retries=3, delay=1, **kwargs):
        """네트워크 오류 시 자동 재시도"""
        for attempt in range(1, retries + 1):
            try:
                return func(*args, **kwargs)
            except (EndpointConnectionError, ClientError) as e:
                if attempt < retries:
                    logger.warning(f"⚠️ S3 재시도 {attempt}/{retries}회: {e}")
                    time.sleep(delay)
                else:
                    logger.error(f"❌ S3 요청 실패 (최대 재시도 초과): {e}")
                    raise

    # 📤 업로드
    def upload_file(self, file_path: str, s3_key: Optional[str] = None) -> Optional[str]:
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return None

        s3_key = s3_key or file_path.name
        try:
            self._retry(
                self.s3.upload_file,
                str(file_path),
                self.bucket_name,
                s3_key,
                ExtraArgs={"ACL": "private"}
            )
            logger.info(f"✅ 업로드 완료: {file_path} → s3://{self.bucket_name}/{s3_key}")
            return f"s3://{self.bucket_name}/{s3_key}"
        except Exception as e:
            logger.exception(f"S3 업로드 실패: {e}")
            return None

    # 📥 다운로드
    def download_file(self, s3_key: str, local_path: str) -> Optional[Path]:
        local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self._retry(
                self.s3.download_file,
                self.bucket_name,
                s3_key,
                str(local_path)
            )
            logger.info(f"📥 다운로드 완료: s3://{self.bucket_name}/{s3_key} → {local_path}")
            return local_path
        except Exception as e:
            logger.exception(f"S3 다운로드 실패: {e}")
            return None

    # ❌ 삭제
    def delete_file(self, s3_key: str) -> bool:
        try:
            self._retry(self.s3.delete_object, Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"🗑️ 삭제 완료: s3://{self.bucket_name}/{s3_key}")
            return True
        except Exception as e:
            logger.exception(f"S3 삭제 실패: {e}")
            return False

    # 🔗 presigned URL
    def generate_presigned_url(self, s3_key: str, expires_in: int = 3600) -> Optional[str]:
        if expires_in > 3600:
            expires_in = 3600  # ⚠️ 보안상 1시간 이상 금지
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_key},
                ExpiresIn=expires_in,
            )
            if not url.startswith("https://"):
                logger.warning("⚠️ Presigned URL이 HTTPS가 아닙니다.")
            logger.info(f"🔗 Presigned URL 생성: {url}")
            return url
        except Exception as e:
            logger.exception(f"URL 생성 실패: {e}")
            return None


# ✅ 싱글톤 인스턴스
s3_service = S3Service()
