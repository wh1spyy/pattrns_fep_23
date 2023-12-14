import unittest
from unittest.mock import MagicMock, patch
import uuid
from port import  Port
from item import  BasicItem



class TestBasicItem(unittest.TestCase):

    def test_get_total_weight(self):

        item = BasicItem(weight=10.0, count=2, containerID=uuid.uuid4())
        expected_total_weight = 10.0 * 1.5
        self.assertEqual(item.get_total_weight(), expected_total_weight)

class TestPort(unittest.TestCase):

    def test_get_distance(self):
        port1 = Port(port_id="Port1", latitude=2.0, longitude=2.0)
        port2 = Port(port_id="Port2", latitude=1.0, longitude=1.0)

        with patch('port.Port.get_distance') as mock_get_distance:

            mock_get_distance.return_value = 100.0

            distance = port1.get_distance(port2)
            expected_distance = 100.0
            self.assertEqual(distance, expected_distance)

if __name__ == "__main__":
    unittest.main()
