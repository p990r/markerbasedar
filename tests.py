'''
This class provides unit testing to graphics functions
'''

import graphics
import unittest

class MyTest(unittest.TestCase):
    try:
        files = graphics.get_files('images')
        img = graphics.get_img(files[0])
        dimensions = graphics.get_shape(img)
    except:
        print('Error: Wrong path or no image files')
        img = None

    def test_get_shape(self):
        self.assertEqual(self.img.shape[0:2],graphics.get_shape(self.img))

    def test_resize_image(self):
        self.dimensions = graphics.get_shape(self.img)
        percentage = 10
        new_dimensions = (int(percentage * self.dimensions[0]/100), int(percentage * self.dimensions[1]/100))
        self.assertEqual(new_dimensions, graphics.get_shape(graphics.resize_image(self.img, percentage)))

    def test_resize_poster(self):
        top_left = (0,0)
        bot_right = (10,10)
        self.assertEqual(bot_right[0]-top_left[0], min(graphics.get_shape(graphics.resize_poster(self.img, top_left, bot_right))))

    def test_pixel_diff(self):
        self.assertEqual((10,15), graphics.pixel_diff(5, 15, 5))
        self.assertEqual((0, 15), graphics.pixel_diff(0, 10, 15))

    def test_set_coords(self):
        index = 0
        top_left = (0, 0)
        bot_right = (10, 10)
        dim1 = 640
        dim2 = 480
        diff = 5
        self.assertEqual((0, 10, 0, 12),graphics.set_coords(index, top_left, bot_right, dim1, dim2, diff))

if __name__ == '__main__':
    unittest.main()