import cv2
import numpy as np
import urllib



def segment(image):



	height, width, depth = image.shape



	''' simple naive grabcut implementation '''
	#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_grabcut/py_grabcut.html#grabcut

	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)

	rect = (.1 * height, .1 * width, .9 * height, .9 * width)
	rect = tuple(int(val) for val in rect)

	mask = np.zeros(image.shape[:2], np.uint8)

	cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

	mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	# image_out = image*mask2[:,:,np.newaxis]

	return image, mask2



	# mask = np.zeros(image.shape[:2], np.uint8)

	# bgdModel = np.zeros((1,65), np.float64)
	# fgdModel = np.zeros((1,65), np.float64)

	# rect = (50,50,450,290)
	# cv2.grabCut(image,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

	# mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	# image = image*mask2[:,:,np.newaxis]



	''' this is the complex gmm code '''
	# b,g,r = cv2.split(image)
	# # get the width and height for this image
	# gh, gw = g.shape
	# # reshape into an image 1px high (EM wants a vector)
	# gd = np.reshape(g, (gh*gw, 1))
	# # instantiate the em object
	# em = cv2.EM(2, cv2.EM_COV_MAT_GENERIC)
	# # train our EM model
	# em.train(gd)



def combine(img_a, img_b, img_b_mask, action):


	# if action == 'wearing':

	# make sure we're working with something reasonable
	img_a = resize(img_a)
	img_a_max_dim = getMaxDim(img_a)

	# scale the article of clothing relative to the image wearing it
	img_b = resize(img_b, img_a_max_dim * .3)


	h,w,d = img_a.shape

	x_out = int(w/2.)
	y_out = int(1*h/6.)

	img_out = copyTo(img_a, img_b, img_b_mask, (y_out,x_out))

	return img_out




def resize(image, dim=600):

	h,w,d = image.shape

	if h > dim or w > dim:

		if h > w:
			h_out = dim
			w_out = int(dim/float(h) * w)
		else:
			w_out = dim
			h_out = int(dim/float(w) * h)

		return cv2.resize(image, (int(w_out), int(h_out)))

	return image


def readFromUrl(image_url):

	# read image from url, and save it to /tmp dir
	fpath, image = urllib.urlretrieve(image_url)
	# read into opencv the image that we wrote to the temp dir
	image = cv2.imread(fpath)

	return image


def getMaxDim(image):
	return max(image.shape)


def copyTo(dest, source, mask, pos):

	x,y = pos
	sx, sy, sd = source.shape

	x_start = max(x - int(sx/2.), 0)
	y_start = max(y - int(sy/2.), 0)


	# for i in range(x_start, x_start + sx):
	# 	for j in range(y_start, y_start + sy):
	# 		dest[i][j] = 



	dest[x_start:x_start + sx, y_start:y_start + sy] = source
	return dest
