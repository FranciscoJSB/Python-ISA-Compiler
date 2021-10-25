from PIL import Image
import random

with open("RandomImage.txt", "r") as f:
    content = f.read()
    data = list(content)

    for i in range(len(data)):
        data[i] = int(data[i])
   
    #data = [random.choice((0, 1)) for _ in range(62500)]
    data[:] = [data[i:i + 250] for i in range(0, 62500, 250)]

    img = Image.new('1', (250, 250))
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = data[i][j]

    img.show()
    img.save('image.png')