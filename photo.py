import bing
import cv2
import vision
import lang

import numpy as np



def create(query):

	canvas = np.zeros((1000,1400,3), np.uint8)
	canvas.fill(255)

	cur_img = None

	tokens = lang.parse(query)

	while True:

		if not tokens:
			break

		cur_token = tokens.pop(0)

		if lang.isAction(cur_token):

			cur_action = cur_token

			next_img = bing.getFirstImage(tokens.pop(0))
			next_img = vision.resize(next_img)
			next_img, next_mask = vision.segment(next_img)


			# masked = cv2.bitwise_and(next_img, next_img, mask=next_mask)

			# cv2.imshow('image', masked)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()


			cur_img = vision.combine(cur_img, next_img, next_mask, cur_action)

		else:

			if cur_img is not None:
				canvas = vision.copyTo(canvas, cur_img, None, None)

			cur_img = bing.getFirstImage(cur_token)
			cur_img = vision.resize(cur_img)
			cur_img, mask = vision.segment(cur_img)


	canvas = vision.copyTo(canvas, cur_img, None, None)
	return canvas