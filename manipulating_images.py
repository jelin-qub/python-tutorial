'''You’re going to load an image using Matplotlib,
realize that RGB images are really just width × height × 3 arrays of int8 integers,
manipulate those bytes, and use Matplotlib again to save that modified image once you’re done.'''

import numpy as np
import matplotlib.image as mpimg

img = mpimg.imread("kitty.jpeg")
print(type(img))
print(img.shape)

'''It’s an image with a height of 1299 pixels, a width of 1920 pixels, 
and three channels: one each for the red, green, and blue (RGB) color levels.'''

#Want to see what happens when you drop out the R and G channels? Add this to your script ?
output = img.copy()  # The original image is read-only!
output[:, :, :2] = 0
mpimg.imsave("blue.jpg", output)



'''But now, it’s time to do something a little more useful. 
You’re going to convert this image to grayscale. However, converting to grayscale is more complicated. 
Averaging the R, G, and B channels and making them all the same will give you an image that’s grayscale.
 But the human brain is weird, and that conversion doesn’t seem to handle the luminosity of the colors quite right.

'''
'''You can use the fact that if you output an array with only one channel instead of three, then you can specify a color map,
 known as a cmap in the Matplotlib world. 
If you specify a cmap, then Matplotlib will handle the linear gradient calculations for you.'''

averages = img.mean(axis=2)  # Take the average of each R, G, and B
mpimg.imsave("bad-gray.jpg", averages, cmap="gray")

'''These new lines create a new array called averages, which is a copy of the img array that you’ve flattened along 
axis 2 by taking the average of all three channels.
 You’ve averaged all three channels and outputted something with R, G, and B values equal to that average. 
When R, G, and B are all the same, the resulting color is on the grayscale.'''

'''But you can do better using the luminosity method. 
This technique does a weighted average of the three channels, with the mindset that the color green 
drives how bright an image appears to be, and blue can make it appear darker.
 You’ll use the @ operator, which is NumPy’s operator for doing a traditional two-dimensional array dot product.'''

weights = np.array([0.3, 0.59, 0.11])
grayscale = img @ weights
mpimg.imsave("good-gray.jpg", grayscale, cmap="gray")