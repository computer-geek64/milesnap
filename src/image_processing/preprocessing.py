#!/usr/bin/python3
# preprocessing.py

import cv2
import numpy as np


def average_blur(img, n=5):
    return cv2.blur(img, (n, n))


def median_blur(img, n=5):
    return cv2.medianBlur(img, n)


def gaussian_blur(img, n=5):
    return cv2.GaussianBlur(img, (n, n), 0)


def bilateral_blur(img, d=15, sigma_color=100, sigma_space=100):
    return cv2.bilateralFilter(img, d, sigma_color, sigma_space)


img = cv2.imread("/root/Downloads/gas.jpg") # image.jpg, x1a.png
cv2.imshow("original", img)
cv2.waitKey()

blurred_img = bilateral_blur(img)
cv2.imshow("blurred", blurred_img)
cv2.waitKey()