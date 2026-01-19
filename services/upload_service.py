import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from config.settings import get_settings
from utils.validators import validate_audio_file, validate_image_file

settings = get_settings()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


class UploadService:

    @staticmethod
    def validate_files(song: UploadFile, thumbnail: UploadFile):
        """Validate song and thumbnail files"""
        validate_audio_file(song, settings.MAX_FILE_SIZE)
        validate_image_file(thumbnail, settings.MAX_FILE_SIZE)

    @staticmethod
    def upload_song_file(song: UploadFile, folder: str) -> str:
        """Upload song file to Cloudinary"""
        result = cloudinary.uploader.upload(
            song.file, resource_type="auto", folder=folder
        )
        return result["url"]

    @staticmethod
    def upload_thumbnail_file(thumbnail: UploadFile, folder: str) -> str:
        """Upload thumbnail file to Cloudinary"""
        result = cloudinary.uploader.upload(
            thumbnail.file, resource_type="image", folder=folder
        )
        return result["url"]

    @staticmethod
    def upload_song_files(
        song: UploadFile, thumbnail: UploadFile, song_id: str
    ) -> tuple[str, str]:
        """Upload both song and thumbnail files"""
        folder = f"songs/{song_id}"

        song_url = UploadService.upload_song_file(song, folder)
        thumbnail_url = UploadService.upload_thumbnail_file(thumbnail, folder)

        return song_url, thumbnail_url
