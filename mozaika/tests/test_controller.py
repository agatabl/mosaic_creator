import sys
sys.path.insert(0, "../")
import unittest
import controller



class TestController(unittest.TestCase):

    def test_urls_to_list(self):
        text = 'ab,na,mn'
        _list = ['ab', 'na', 'mn']
        self.assertEqual(controller.urls_to_list(text, None), _list)
        self.assertIsNot(controller.urls_to_list(text, 1), _list)

    def test_resolution_params(self):
        param = '1000x345'
        param_lst = [1000, 345]
        self.assertEqual(controller.resolution_params(param), param_lst)
        self.assertEqual(controller.resolution_params(None), [2048,2048])

    def test_img_height(self):
        eq_images_lst = ['aa', 'bb', 'cc', 'dd']
        odd_images_lst = ['aa', 'bb', 'cc']
        parent_height = 1000
        self.assertEqual(controller.img_height(eq_images_lst,parent_height), int(1000/(4//2)))
        self.assertEqual(controller.img_height(odd_images_lst,parent_height), int(1000/(3//2+1)))


if __name__ == '__main__':
    unittest.main()
