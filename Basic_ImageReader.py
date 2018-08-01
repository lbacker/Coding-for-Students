from PIL import Image
from PIL import ImageEnhance
import math

# Completely different color
def diff_color( image ):
    width,height=img.size

    # Process every pixel
    for x in range(width):
        for y in range(height):
            new_color = (0,100,100)
            image.putpixel( (x,y), new_color)
    return image

# Remove single color (red)
def remove_color( image, color ):
    width,height=img.size

    # Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = img.getpixel( (x,y) )
            if color == "red":
                new_color = (0,) + current_color[1:]
            if color == "green":
                new_color = current_color[:1] + (0,) +  current_color[2:]
            if color == "blue":
                new_color = current_color[0:2] + (0,)
            image.putpixel( (x,y), new_color)
    return image

# Get color of specified pixel
def get_pixel( image, x, y ):
    pix = image.load()
    print pix[x,y]
    return pix[x,y]

# Resize image
def resize( image, size1, size2 ):
    new_img = image.resize((size1,size2))
    return new_img

# Convert to grayscale (using 'grayscale' function on Wikipedia)
def rgb2gray(image):
    width,height=img.size

    # Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = img.getpixel( (x,y) )
            scaling_function = (0.299, 0.587, 0.114)
            new_color = int(sum([a*b for a,b in zip(current_color,scaling_function)]))
            image.putpixel( (x,y), (new_color, new_color, new_color))
    return image

def horse_vision(img, slices):
    slices = 2
    offset = 40
    width, height = img.size
    slice_size = int(width/slices)
    
    # Left half
    print int(slice_size) - offset
    print 2*offset
    print slice_size + offset
    bbox = (0, 0, slice_size - offset, height)
    slice_left = img.crop(bbox)

    # Black box
    slice_black = Image.new('RGB', (2*offset, height), (0,0,0))
    
    # Right half
    bbox = (slice_size + offset, 0, width, height)
    slice_right = img.crop(bbox)

    # New width and height
    new_im = Image.new('RGB', (width, height))
    
    x_offset = 0
    for im in (slice_left, slice_black, slice_right):
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    return new_im

        
############################
# Start actual Python Script
############################
if __name__ == '__main__':

    img = Image.open('spring.jpg') 

    # Function calls here
    #img = diff_color(img) 
    #img = resize(img,100,100)
    #img = rgb2gray(img)
    #img = remove_color(img,"green")
    #img = horse_vision(img,2)
    #img = ImageEnhance.Sharpness(img).enhance(4)
    
    # Displaying
    img.show()

    # Saving
    #img.save('new_image','png')



