from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from links.views import redis_test_db


class PostRequestValidTest(APITestCase):
    """Тестируем валидный POST-запрос к visited_links/."""

    @classmethod
    def setUpClass(cls):
        """Данные для тестов."""
        super().setUpClass()
        cls.db_obj_before = len(redis_test_db.keys()) - \
            redis_test_db.exists("list_of_keys")
        cls.client = APIClient()
        cls.url = reverse("visited_links")
        cls.request = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit"
            ]
        }

        cls.response = cls.client.post(
            cls.url, cls.request, format="json", HTTP_TEST="True")
        cls.last_entry = redis_test_db.lindex("list_of_keys", -1)
        cls.set_of_domains = redis_test_db.smembers(str(cls.last_entry))

    def test_status(self):
        """Успешный POST-запрос к visited_links/ возвращает статус 201."""
        self.assertEqual(PostRequestValidTest.response.status_code, 201)

    def test_db(self):
        """В базу добавляется один объект."""
        db_obj_after = len(redis_test_db.keys())
        self.assertEqual(db_obj_after, PostRequestValidTest.db_obj_before + 2)
        self.assertEqual(redis_test_db.llen("list_of_keys"), len(
            redis_test_db.keys()) - redis_test_db.exists("list_of_keys"))

    def test_response(self):
        """При успешном запросе возвращается ожидаемый ответ."""
        expected_response = {"status": "ok"}
        self.assertEqual(PostRequestValidTest.response.json(),
                         expected_response)

    def test_unique_domains(self):
        """В базу сохраняются только уникальные домены."""
        self.assertEqual(len(PostRequestValidTest.set_of_domains), 3)

    def test_domains(self):
        """В базу сохраняются домены, а не ссылки."""
        domain = "stackoverflow.com"
        self.assertEqual(domain in PostRequestValidTest.set_of_domains, True)

    @classmethod
    def tearDownClass(cls):
        """Удаляем созданные данные из базы."""
        for key in redis_test_db.keys():
            redis_test_db.delete(key)


class PostRequestInvalidTest(APITestCase):
    """Тестируем ошибочный POST-запрос к visited_links/."""

    @classmethod
    def setUpClass(cls):
        """Данные для тестов."""
        super().setUpClass()
        cls.client = APIClient()
        cls.url = reverse("visited_links")

    def test_empty_request(self):
        """При отправке пустого списка ссылок возникает ошибка."""
        request = {
            "links": []
        }
        response = PostRequestInvalidTest.client.post(
            PostRequestInvalidTest.url,
            request, format="json", HTTP_TEST="True"
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_link(self):
        """Возникает ошибка, если хотя бы у одной из ссылок
        в запросе неправильный формат."""
        request = {
            "links": [
                "https://yaru",
                "funbox.ru",
            ]
        }
        response = PostRequestInvalidTest.client.post(
            PostRequestInvalidTest.url,
            request, format="json", HTTP_TEST="True"
        )
        self.assertEqual(response.status_code, 400)
