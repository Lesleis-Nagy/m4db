import unittest
import xmlrunner

from m4db_database.rest_api.m4db_runner_web.is_alive import is_alive


class TestIsAlive(unittest.TestCase):

    def test_is_alive(self):
        result = is_alive()
        assert result is True


if __name__ == "__main__":
    with open("test-is-alive.xml", "wb") as fout:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=fout),
            failfast=False, buffer=False, catchbreak=False
        )
