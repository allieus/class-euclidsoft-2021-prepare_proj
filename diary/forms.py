from io import BytesIO
from typing import Optional

from PIL import Image as PILImage
from django import forms
from django.core.files.uploadedfile import UploadedFile

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["message", "photo"]

    def clean_photo(self):
        photo: Optional[UploadedFile] = self.cleaned_data.get("photo")

        if photo:
            pil_image: PILImage = PILImage.open(photo)
            # 썸네일 처리 및 exif 헤더 제거
            pil_image.thumbnail((512, 512))
            thumbnail_photo = BytesIO()
            thumbnail_photo.name = photo.name
            pil_image.save(thumbnail_photo)
            return UploadedFile(thumbnail_photo)

        return photo
