import time

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from links.views import redis_test_db


class GetRequestTest(APITestCase):
    """Тестируем GET-запрос к visited_domains/."""

    @classmethod
    def setUpClass(cls):
        """Данные для тестов."""
        super().setUpClass()
        cls.client = APIClient()
        cls.url_post = reverse("visited_links")
        cls.url_get = reverse("visited_domains")
        cls.request_post_1 = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru"
            ]
        }
        cls.response_post_1 = cls.client.post(
            cls.url_post, cls.request_post_1, format="json", HTTP_TEST="True")
        time.sleep(5)
        cls.request_post_2 = {
            "links": [
                "https://stackoverflow.com/questions/11828270/how-to"
            ]
        }
        cls.response_post_2 = cls.client.post(
            cls.url_post, cls.request_post_2, format="json", HTTP_TEST="True")
        test_from = str(redis_test_db.lindex("list_of_keys", -1))
        test_to = str(int(test_from) + 5)
        cls.params = {"from": test_from, "to": test_to}

    def test_status(self):
        """Успешный GET-запрос к visited_domains/ возвращает статус 200."""
        response_get = GetRequestTest.client.get(
            GetRequestTest.url_get, GetRequestTest.params, HTTP_TEST="True")
        self.assertEqual(response_get.status_code, 200)

    def test_response(self):
        """При успешном запросе возвращается ожидаемый ответ."""
        response_get = GetRequestTest.client.get(
            GetRequestTest.url_get, GetRequestTest.params, HTTP_TEST="True")
        expected_response = {
            "domains": [
                "stackoverflow.com"
            ],
            "status": "ok"
        }
        self.assertEqual(response_get.json(), expected_response)

    def test_no_params(self):
        """Запрос не обрабатывается, если не переданы параметры from и to."""
        response_get = GetRequestTest.client.get(
            GetRequestTest.url_get, HTTP_TEST="True")
        self.assertEqual(response_get.status_code, 400)

    def test_invalid_params(self):
        """Запрос не обрабатывается,
        если передан неправильный формат параметров from и to."""
        params = {"from": "01.09.2021", "to": "02.09.2021"}
        response_get = GetRequestTest.client.get(
            GetRequestTest.url_get, params, HTTP_TEST="True")
        self.assertEqual(response_get.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        """Удаляем созданные данные из базы."""
        for key in redis_test_db.keys():
            redis_test_db.delete(key)
