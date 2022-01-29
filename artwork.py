from PIL import Image

def scale(file):
    image = Image.open(file)
    new_image = image.resize((250, 250))
    new_image.save(file)


if __name__ == '__main__':
    import os
    for i in os.listdir('web/Library/Covers'):
        scale(os.path.join('web/Library/Covers/', i))