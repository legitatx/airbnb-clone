from cloudinary import config as cloudinary_init, uploader
from os import getenv

api_key: str = getenv("CLOUDINARY_KEY")
api_secret: str = getenv("CLOUDINARY_SECRET")
cloud_name: str = getenv("CLOUDINARY_NAME")

cloudinary_init(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)


async def upload(image: str):
    async_kwarg = {"async": True}
    res = uploader.upload(image, **async_kwarg, folder="RBNB_Assets/")
    return res["secure_url"]
