#having lots of trouble as talked about in the article, its just not closed enough for fill holes to do the job

#http://scikit-image.org/docs/dev/user_guide/tutorial_segmentation.html
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image
from skimage.color import label2rgb
from skimage.feature import canny

# L converts to 8-bit pixels, black and white
# http://pillow.readthedocs.io/en/3.2.x/handbook/concepts.html#concept-modes
im = np.array(Image.open('./Drop 2.png').convert('L'))

#why /255.  I think its just divinding by 255 as a float?
# edges = canny(im/255.)

#canny http://scikit-image.org/docs/dev/api/skimage.feature.html#skimage.feature.canny
#all trial and error, this probably isnt the best
edges = canny(im, sigma=3, low_threshold=40, high_threshold=50)

# now that we have some edges, fill holes for feature detection
fillled = ndi.binary_fill_holes(edges)

#label features
label_objects, nb_labels = ndi.label(fillled)

#count size of features
sizes = np.bincount(label_objects.ravel())

#get only the sizes equal to the max size
mask_sizes = (sizes == np.amax(sizes))

#apply only the one feature back onto the label array
single_feature = mask_sizes[label_objects]

#overlay our single feature on the the original image
image_label_overlay = label2rgb(single_feature, image=im)





fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(8, 3),
                                    sharex=True, sharey=True)


ax1.imshow(im, interpolation='nearest')
ax1.set_title('orig')
ax1.axis('off')
ax1.set_adjustable('box-forced')



ax2.imshow(edges, interpolation='nearest')
ax2.set_title('edges')
ax2.axis('off')
ax2.set_adjustable('box-forced')



ax3.imshow(fillled, interpolation='nearest')
ax3.set_title('filled')
ax3.axis('off')
ax3.set_adjustable('box-forced')


ax4.imshow(image_label_overlay, interpolation='nearest')
ax4.set_title('single feature overlayed')
ax4.axis('off')
ax4.set_adjustable('box-forced')


margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
fig.subplots_adjust(**margins)

plt.show()