import PIL
from PIL import Image
import random
import string


class ImageSize:

    def __init__(self, image, output):
        self.image = image
        self.output = output

    def __size_calculate(height, width):
        if height <= 1200 and width <= 1200:
            h, w = height//2, width//2
        elif height <= 2000 and width <= 2000:
            h, w = height//4, width//4
        elif height <= 5000 and width <= 5000:
            h, w = height//5, width//5
        else:
            h, w = height//6, width//6
        return h, w

    def size_reducer(self):
        img = Image.open(self.image)
        img = img.convert('RGB')
        h, w = img.size
        h, w = self.__size_calculate(h, w)
        img = img.resize((h, w), Image.ANTIALIAS)
        name = ''.join(random.sample(string.digits+string.digits, 20))+'.jpg'
        img.save(f'{self.output}{name}.jpg')
