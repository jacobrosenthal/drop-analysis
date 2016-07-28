#could see this working, but noiser than histo atm


# http://scikit-image.org/docs/dev/auto_examples/plot_contours.html
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from PIL import Image

# L converts to 8-bit pixels, black and white
# http://pillow.readthedocs.io/en/3.2.x/handbook/concepts.html#concept-modes
r = np.array(Image.open('./Drop 2.png').convert('L'))

#find_contours http://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.find_contours
# not guaranteed to be the best number, I just started poking nubmers, seems to be very similar to histogram
contours = measure.find_contours(r, 100)

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(r, interpolation='nearest', cmap=plt.cm.gray)

print contours
for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()