from fastapi.testclient import TestClient
import unittest
from src.main import app
from unittest.mock import MagicMock, patch

class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Create a test client before each test case.
        """
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        """
        Close the test client after all test cases.
        """
        cls.client.close()

    @patch('subprocess.run')
    def test_sends_dispatches_awake_on_valid_mac_address(self, mock_subprocess):
        result = "Sending magic packet to 255.255.255.255 with broadcast 255.255.255.255 MAC 02-42-5B-3A-A8-9A port 9\n"

        mock_stdout = MagicMock()
        mock_stdout.configure_mock(
            **{
                "stdout.decode.return_value": result,
                "stderr.decode.return_value": None
            }
        )
        mock_subprocess.return_value = mock_stdout

        mac = "02:42:5b:3a:a8:9a"
        response = self.client.post("/", json={"mac": mac})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": result})

        mock_subprocess.assert_called_once_with(["awake", mac], capture_output=True)

    @patch('subprocess.run')
    def test_mac_address_is_required(self, mock_subprocess):
        response = self.client.post("/", json={"ip": "192.168.0.1"})

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": "Missing 'mac' field in request body"})

        mock_subprocess.assert_not_called()

    @patch('subprocess.run')
    def test_mac_address_must_be_correct(self, mock_subprocess):
        response = self.client.post("/", json={"mac": "192.168.0.1"})

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": "Invalid MAC address format"})

        mock_subprocess.assert_not_called()

    def test_health_check_returns_correct_status(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "OK"})

if __name__ == '__main__':
    unittest.main()