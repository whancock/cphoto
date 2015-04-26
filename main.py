import photo
import cv2

# canvas = photo.create('a cat and irfan+essa wearing a blue+hat and steve+jobs wearing a blue+elephant')
# canvas = photo.create('an elephant wearing a monkey wearing a hat and irfan+essa wearing a monkey')

canvas = photo.create('aaron+bobick wearing a red+hat')


cv2.imshow('image', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()