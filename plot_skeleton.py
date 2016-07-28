#need an array of only zeros and ones, we could histogram I guess, but then dont need skeletonize

# http://scikit-image.org/docs/dev/auto_examples/plot_skeleton.html
from skimage.morphology import skeletonize
from skimage import draw
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
# L converts to 8-bit pixels, black and white
# http://pillow.readthedocs.io/en/3.2.x/handbook/concepts.html#concept-modes
image = np.array(Image.open('./Drop 2.png').convert('L'))

# perform skeletonization
skeleton = skeletonize(image)

# display results
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4.5),
                               sharex=True, sharey=True,
                               subplot_kw={'adjustable': 'box-forced'})

ax1.imshow(image, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('original', fontsize=20)

ax2.imshow(skeleton, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('skeleton', fontsize=20)

fig.tight_layout()

plt.show()
