import unittest
import sorter

class TestBubble(unittest.TestCase):
    def test_bubble_sorted(self):
        arr = [16, 40, 52, 71, 86]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.bubbleSort(arr), sort_arr)
    def test_bubble_reversed(self):
        arr = [86, 71, 52, 40, 16]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.bubbleSort(arr), sort_arr)
    def test_bubble_empty(self):
        arr = []
        sort_arr = []
        self.assertEqual(sorter.Sorter.bubbleSort(arr), sort_arr)
    def test_bubble_one_element(self):
        arr = [42]
        sort_arr = [42]
        self.assertEqual(sorter.Sorter.bubbleSort(arr), sort_arr)
    def test_bubble_all_negative(self):
        arr = [-3, -1, -7, -4]
        sort_arr = [-7, -4, -3, -1]
        self.assertEqual(sorter.Sorter.bubbleSort(arr), sort_arr)
    def test_bubble_random(self):
        arr = [3, -2, 5, 1, 0, -4]
        sort_arr = [-4, -2, 0, 1, 3, 5]
        self.assertEqual(sorter.Sorter.bubbleSort(arr), sort_arr)

class TestInsertion(unittest.TestCase):
    def test_insertion_sorted(self):
        arr = [16, 40, 52, 71, 86]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.insertionSort(arr), sort_arr)
    def test_insertion_reversed(self):
        arr = [86, 71, 52, 40, 16]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.insertionSort(arr), sort_arr)
    def test_insertion_empty(self):
        arr = []
        sort_arr = []
        self.assertEqual(sorter.Sorter.insertionSort(arr), sort_arr)
    def test_insertion_one_element(self):
        arr = [42]
        sort_arr = [42]
        self.assertEqual(sorter.Sorter.insertionSort(arr), sort_arr)
    def test_insertion_all_negative(self):
        arr = [-3, -1, -7, -4]
        sort_arr = [-7, -4, -3, -1]
        self.assertEqual(sorter.Sorter.insertionSort(arr), sort_arr)
    def test_insertion_random(self):
        arr = [3, -2, 5, 1, 0, -4]
        sort_arr = [-4, -2, 0, 1, 3, 5]
        self.assertEqual(sorter.Sorter.insertionSort(arr), sort_arr)

class TestMerge(unittest.TestCase):
    def test_merge_sorted(self):
        arr = [16, 40, 52, 71, 86]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.mergeSort(arr), sort_arr)
    def test_merge_reversed(self):
        arr = [86, 71, 52, 40, 16]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.mergeSort(arr), sort_arr)
    def test_merge_empty(self):
        arr = []
        sort_arr = []
        self.assertEqual(sorter.Sorter.mergeSort(arr), sort_arr)
    def test_merge_one_element(self):
        arr = [42]
        sort_arr = [42]
        self.assertEqual(sorter.Sorter.mergeSort(arr), sort_arr)
    def test_merge_all_negative(self):
        arr = [-3, -1, -7, -4]
        sort_arr = [-7, -4, -3, -1]
        self.assertEqual(sorter.Sorter.mergeSort(arr), sort_arr)
    def test_merge_random(self):
        arr = [3, -2, 5, 1, 0, -4]
        sort_arr = [-4, -2, 0, 1, 3, 5]
        self.assertEqual(sorter.Sorter.mergeSort(arr), sort_arr)

class TestQuick(unittest.TestCase):
    def test_quick_sorted(self):
        arr = [16, 40, 52, 71, 86]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.quickSort(arr), sort_arr)
    def test_quick_reversed(self):
        arr = [86, 71, 52, 40, 16]
        sort_arr = [16, 40, 52, 71, 86]
        self.assertEqual(sorter.Sorter.quickSort(arr), sort_arr)
    def test_quick_empty(self):
        arr = []
        sort_arr = []
        self.assertEqual(sorter.Sorter.quickSort(arr), sort_arr)
    def test_quick_one_element(self):
        arr = [42]
        sort_arr = [42]
        self.assertEqual(sorter.Sorter.quickSort(arr), sort_arr)
    def test_quick_all_negative(self):
        arr = [-3, -1, -7, -4]
        sort_arr = [-7, -4, -3, -1]
        self.assertEqual(sorter.Sorter.quickSort(arr), sort_arr)
    def test_quick_random(self):
        arr = [3, -2, 5, 1, 0, -4]
        sort_arr = [-4, -2, 0, 1, 3, 5]
        self.assertEqual(sorter.Sorter.quickSort(arr), sort_arr)

        
if __name__ == "__main__":
    unittest.main()
