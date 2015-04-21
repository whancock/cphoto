import bing
import cv2
import vision
import lang

import numpy as np



def create(query):

	canvas = np.zeros((800,1200,3), np.uint8)
	canvas.fill(255)

	tokens = lang.parse(query)

	cur_img = bing.getFirstImage(tokens.pop(0))
	cur_img = vision.resize(cur_img)
	cur_img, mask = vision.segment(cur_img)

	while True:

		if not tokens:
			break

		cur_token = tokens.pop(0)

		if lang.isAction(cur_token):

			cur_action = cur_token

			next_img = bing.getFirstImage(tokens.pop(0))
			next_img = vision.resize(next_img)
			next_img, next_mask = vision.segment(next_img)


			cur_img = vision.combine(cur_img, next_img, next_mask, cur_action)

		else:
			#write cur_img to the canvas
			canvas = vision.copyTo(canvas, cur_img, None, (400,600))

	canvas = vision.copyTo(canvas, cur_img, None, (400,600))
	return canvas