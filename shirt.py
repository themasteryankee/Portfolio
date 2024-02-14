import sys
from PIL import Image, ImageOps, ImageFilter
from PIL.Image import Resampling

#Takes 2 command-line arguments.
#First one for image input file
#Second one for image output file
if len(sys.argv) > 3:
    print("Too many command-line arguments")
    sys.exit(1)
elif len(sys.argv) < 3:
    print("Too few command-line arguments")
    sys.exit(1)
elif not sys.argv[1].endswith(".jpeg") and not sys.argv[1].endswith(".png") and not sys.argv[1].endswith(".jpg"):
    print("Invalid input")
    sys.exit(1)
elif not sys.argv[2].endswith(".jpeg") and not sys.argv[2].endswith(".png") and not sys.argv[2].endswith(".jpg"):
    print("Invalid input")
    sys.exit(1)

#Checks extensions
pre, extension = sys.argv[1].split(".")
suf, extension2 =sys.argv[2].split(".")

if extension != extension2:
    print("Input and output have different extensions")
    sys.exit(1)
    
#Saves new output image
try:
    shirt = Image.open("shirt.png")
    size = shirt.size
    person = Image.open(sys.argv[1])
    person = ImageOps.fit(person, size, method=Resampling.BICUBIC, bleed=0.0, centering=(0.5, 0.5))
    output = person.paste(shirt, (0,0), mask=shirt)

    person.save(sys.argv[2])
except FileNotFoundError:
    print("Input does not exist")
    sys.exit(1)
