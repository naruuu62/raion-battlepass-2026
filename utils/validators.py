from fastapi import HTTPException, UploadFile
from utils.const import ALLOWED_AUDIO_TYPES, ALLOWED_IMAGE_TYPES


def validate_file_type(file: UploadFile, allowed_types: list, file_label: str):
    """Validate file content type"""
    if file.content_type not in allowed_types:
        raise HTTPException(400, detail=f"Invalid {file_label} file type")


def validate_file_size(file: UploadFile, max_size: int, file_label: str):
    """Validate file size"""
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > max_size:
        raise HTTPException(
            400,
            detail=f"{file_label} file too large. Max size: {max_size / (1024 * 1024)}MB",
        )


def validate_audio_file(file: UploadFile, max_size: int):
    """Validate audio file type and size"""
    validate_file_type(file, ALLOWED_AUDIO_TYPES, "audio")
    validate_file_size(file, max_size, "Audio")


def validate_image_file(file: UploadFile, max_size: int):
    """Validate image file type and size"""
    validate_file_type(file, ALLOWED_IMAGE_TYPES, "image")
    validate_file_size(file, max_size, "Thumbnail")
