from django.db import models


class Link(models.Model):
    visit_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    link = models.CharField("Ссылка", max_length=1000)

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"
        ordering = ("-visit_date",)

    def __str__(self):
        return self.link
