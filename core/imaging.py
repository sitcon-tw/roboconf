from wand.image import Image

def resize_image(image_file, size):
    # Throws ValueError on bad image, according to Wand.py docs
    with Image(file=image_file) as image:
        # Crop to square image first
        if image.width > image.height:
            x = (image.width - image.height) / 2
            image.crop(left=x, width=image.height)
        elif image.height > image.width:
            y = (image.height - image.width) / 2
            image.crop(top=y, height=image.width)

        if image.width > size:
            image.resize(width=size, height=size)

        return (image.make_blob(), image.mimetype)
