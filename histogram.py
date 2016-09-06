#suprisingly good

#http://scikit-image.org/docs/dev/user_guide/tutorial_segmentation.html
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image
from skimage.color import label2rgb
from skimage import feature
import numpy.polynomial.polynomial as poly


# L converts to 8-bit pixels, black and white
# http://pillow.readthedocs.io/en/3.2.x/handbook/concepts.html#concept-modes
im = np.array(Image.open('./Drop 1.png').convert('L'))
# print "im, ", im

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

# print "edges, ", edges

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

# print "mask_sizes, ", mask_sizes

#apply only the one feature back onto the label array
single_feature = mask_sizes[label_objects]

# print "single feature, ", single_feature

#overlay our single feature on the the original image
image_label_overlay = label2rgb(single_feature, image=im)


masked = np.bitwise_and(im, single_feature);
# print "masked, ", masked


# really dont understand why but when treated as points it seems rotated and flipped?
flip_masked=np.rot90(masked)
flip_masked=np.flipud(flip_masked)
point_list=np.argwhere(flip_masked>0)
# print "point_list, ", point_list

#find the top curve by finding the largets y value for each x
#not sure how to do this without an intermediate associative array topcurveDict
topcurveDict = {}
for i, val in enumerate(point_list):
  x=val[0]
  y=val[1]
  if x not in topcurveDict or topcurveDict[x] > y:
    topcurveDict[x]=y

#turn topcurveDict back into a numpy array of numpy arrays of points
top_point_list = np.array(topcurveDict.items(), dtype=int)
x_list_top = top_point_list[:,0]
y_list_top = top_point_list[:,1]


#find the bot curve by finding the smallest y value for each x
#not sure how to do this without an intermediate associative array topcurveDict
botcurveDict = {}
for i, val in enumerate(point_list):
  x=val[0]
  y=val[1]
  if x not in botcurveDict or botcurveDict[x] < y:
    botcurveDict[x]=y

#turn botcurveDict back into a numpy array of numpy arrays of points
bot_point_list = np.array(botcurveDict.items(), dtype=int)
x_list_bot = bot_point_list[:,0]
y_list_bot = bot_point_list[:,1]

# print "top_point_list, ", top_point_list
# print "bot_point_list, ", bot_point_list


# https://stackoverflow.com/questions/18767523/fitting-data-with-numpy
coefs_top = poly.polyfit(x_list_top, y_list_top, 4)
print "coefs_top", coefs_top
ffit_top = poly.Polynomial(coefs_top)


coefs_bot = poly.polyfit(x_list_bot, y_list_bot, 4)
print "coefs_bot, ", coefs_bot
ffit_bot = poly.Polynomial(coefs_bot)





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


ax5.plot(x_list_top,y_list_top)
ax5.plot(x_list_top,ffit_top(x_list_top))

ax5.plot(x_list_bot,y_list_bot)
ax5.plot(x_list_bot,ffit_bot(x_list_bot))

ax5.set_title('2 curve fit')
# ax5.set_adjustable('box-forced')


margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
fig.subplots_adjust(**margins)

plt.show()


