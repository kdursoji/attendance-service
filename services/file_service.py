"""
File Service - Business Logic Layer
Following Single Responsibility Principle
"""
from typing import Optional
from flask import current_app
from werkzeug.datastructures import FileStorage
from util.cloud_utils import upload_file_to_s3


class FileService:
    """File Service - Single Responsibility: Handle file operations"""
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        if not filename:
            return False
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def upload_profile_picture(self, file: FileStorage) -> Optional[str]:
        """Upload profile picture to S3"""
        if not file or not self.is_allowed_file(file.filename):
            return None
        
        bucket = current_app.config.get("S3_BUCKET")
        if not bucket:
            return None
        
        try:
            return upload_file_to_s3(bucket, file)
        except Exception:
            return None

