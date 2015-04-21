import bing
import cv2
import vision
import lang

import numpy as np



def create(query):

	canvas = np.zeros((1000,1400,3), np.uint8)
	canvas_mask = np.ones((1000,1400,3), np.uint8)
	canvas.fill(255)

	cur_img = None
	cur_img_mask = None

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


			cur_img, cur_img_mask = vision.combine(cur_img, cur_img_mask, next_img, next_mask, cur_action)

		else:

			if cur_img is not None:
				canvas, canvas_mask = vision.copyTo(canvas, canvas_mask, cur_img, cur_img_mask, None)

			cur_img = bing.getFirstImage(cur_token)
			cur_img = vision.resize(cur_img)
			cur_img, cur_img_mask = vision.segment(cur_img)


	canvas, canvas_mask = vision.copyTo(canvas, canvas_mask, cur_img, cur_img_mask, None)
	return canvas