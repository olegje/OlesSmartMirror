from PIL import Image



path = "test/sym/images.png"

src_im = Image.open(path)
angle0 = int(float("180"))
angle=(360 - angle0)
size = (100, 100)
rot = src_im.rotate( angle, expand=1 ).resize(size)
rot.show()
rot.save("test/sym/images2s.png")
