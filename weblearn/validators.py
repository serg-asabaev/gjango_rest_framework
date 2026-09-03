from rest_framework.serializers import ValidationError
import re
from urllib.parse import urlparse

ALLOWED_VIDEO_DOMAINS = [
    'youtube.com',
    'www.youtube.com',
    'm.youtube.com',
    'youtu.be',
    'youtube-nocookie.com',
]

class LessonLinkValidator:

    def __call__(self, url):
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower().replace('www.', '')
        except Exception:
            raise ValidationError('Некорректная ссылка.')

        if domain not in ALLOWED_VIDEO_DOMAINS:
            raise ValidationError(
                f'Разрешены только ссылки на YouTube. Получен домен: {domain}',
                code='invalid_video_host'
            )