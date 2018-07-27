from PIL import Image

im = Image.open('123.jpg')

w , h = im.size

print('original image size:%s*%s' % (w , h))

im.thumbnail((w//2 , h//2))
print('resize image to:%s*%s' % (w//2 , h//2))

im.save('thumbnail.jpg' , 'jpeg')