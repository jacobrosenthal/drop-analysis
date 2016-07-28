#havent had any luck with this algo.. need to clean it up first or something

#http://www.scipy-lectures.org/advanced/image_processing/auto_examples/plot_find_edges.html#example-plot-find-edges-py
import numpy as np
import scipy
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image


im = scipy.misc.imread('./Drop 2.png')

# https://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.ndimage.filters.sobel.html
sx = ndi.sobel(im, axis=0, mode='constant')
sy = ndi.sobel(im, axis=1, mode='constant')

sob = np.hypot(sx, sy)

# saw this somewhere...
# sob *= 255.0 / np.max(sob)  # normalize (Q&D)

plt.figure(figsize=(16, 5))
plt.subplot(141)
plt.imshow(im, cmap=plt.cm.gray)
plt.axis('off')
plt.title('original', fontsize=20)
plt.subplot(142)
plt.imshow(sx)
plt.axis('off')
plt.title('Sobel (x direction)', fontsize=20)
plt.subplot(143)
plt.imshow(sob)
plt.axis('off')
plt.title('Sobel filter', fontsize=20)





# sx = ndi.sobel(im, axis=0, mode='constant')
# sy = ndi.sobel(im, axis=1, mode='constant')

# # # now that we have some edges, fill holes for feature detection
# # something = ndi.binary_fill_holes(sx)

# sob = np.hypot(sx, sy)

# plt.subplot(144)
# plt.imshow(sob)
# plt.axis('off')
# plt.title('Sobel filled', fontsize=20)





plt.subplots_adjust(wspace=0.02, hspace=0.02, top=1, bottom=0, left=0, right=0.9)

plt.show()

