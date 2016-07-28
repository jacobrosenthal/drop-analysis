#suprisingly good

#http://scikit-image.org/docs/dev/user_guide/tutorial_segmentation.html
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image
from skimage.color import label2rgb


# L converts to 8-bit pixels, black and white
# http://pillow.readthedocs.io/en/3.2.x/handbook/concepts.html#concept-modes
im = np.array(Image.open('./Drop 1.png').convert('L'))
print "im"
print im

line = 120 #based at looking at a histogram, how to get programmatically?

#do the histogram
# hist, bin_edges = np.histogram(im, bins=60)
# bin_centers = 0.5*(bin_edges[:-1] + bin_edges[1:])

# # cant seem to get this formated into the other graphs so its seperate
# plt.figure(figsize=(11,4))
# plt.subplot(132)
# plt.plot(bin_centers, hist, lw=2)
# plt.axvline(line, color='r', ls='--', lw=2)
# plt.text(0.57, 0.8, 'histogram', fontsize=20, transform = plt.gca().transAxes)
# plt.yticks([])
# plt.subplots_adjust(wspace=0.02, hspace=0.3, top=1, bottom=0.1, left=0, right=1)

# plt.show()


#THIS is the 'edge detection' bit, look where most of your pixels fall
#in our case theres drop offs after 30 and like 85
#then going above that can clean up some edges
edges = im > 120 #looking at a histogram helps you see wehre most stuff is

print "edges"
print edges
# now that we have some edges, fill holes for feature detection
fillled = ndi.binary_fill_holes(edges)

#label features
label_objects, nb_labels = ndi.label(fillled)

#count size of features
sizes = np.bincount(label_objects.ravel())

#get only the sizes equal to the max size
# for some reason == produces what I would consider inverted, so swap it
# mask_sizes = (sizes != np.amax(sizes))

#another method, biggest is always first element
mask_sizes = (sizes != sizes[0])

print "mask_sizes"
print mask_sizes

#apply only the one feature back onto the label array
single_feature = mask_sizes[label_objects]

print "single feature"
print single_feature

#overlay our single feature on the the original image
image_label_overlay = label2rgb(single_feature, image=im)


masked = np.bitwise_and(im, single_feature);

print "masked"
print masked


lefty = left[0]
righty = right[0]
#remember higher number, higher in photo
print "left"
print lefty
print "right"
print righty
#if lefty is higher, rotate left
if(lefty>righty)
  ndi.interpolation.rotate(masked)

#if rig is higher, rotate right
if(righty>lefty)
  ndi.interpolation.rotate(masked)




left = None
top = None
right = None
bottom = None
first = True
it = np.nditer(masked, flags=['multi_index'])
while not it.finished:
  while 1:
    if(it[0]):
      # the first pixel we find is the default minima and maxima on both axes
      if first:
        left = it.multi_index
        right = it.multi_index
        bottom = it.multi_index
        top = it.multi_index
        first = False
        break
      y = it.multi_index[0]
      x = it.multi_index[1]
      # if x is less than left, its a new left
      if(x<left[1]):
        left = it.multi_index
      # if x is larger than right, its a new right
      if(x>right[1]):
        right = it.multi_index
      # if y is greater than bottom, its a new bottom
      if(y>bottom[0]):
        bottom = it.multi_index
      # were starting from top so there cant be a more top point
      break
    break
  it.iternext()



fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=1, ncols=5, figsize=(8, 3),
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


ax5.imshow(masked, interpolation='nearest')
ax5.set_title('masked')
ax5.axis('off')
ax5.set_adjustable('box-forced')
circ = plt.Circle((top[1], top[0]), radius=10, color='b')
circ2 = plt.Circle((bottom[1], bottom[0]), radius=10, color='b')
circ3 = plt.Circle((right[1], right[0]), radius=10, color='g')
circ4 = plt.Circle((left[1], left[0]), radius=10, color='g')
ax5.add_patch(circ)  
ax5.add_patch(circ2)  
ax5.add_patch(circ3)  
ax5.add_patch(circ4)  

from matplotlib.patches import Ellipse


r = top[1] - left[1]
c = plt.Circle((top[1], top[0]), r, color='r', linewidth=2, fill=False)
ax5.add_patch(c)


ellipse = Ellipse(xy=(top[1], top[0]), width=0.036, height=0.012, 
                        edgecolor='r', fc='None', lw=2)
ax5.add_patch(ellipse)



margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
fig.subplots_adjust(**margins)

plt.show()


