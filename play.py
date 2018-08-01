from PIL import Image
import ColourEdit as CE


img = Image.open('spring.jpg')
img.show()

img = CE.rg_color_blind(img, "Blue", "Purple", delta=50)
img.show()

# img = CE.horse_vision(img)
# img.show()
