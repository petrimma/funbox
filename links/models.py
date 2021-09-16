from django.db import models


class Link(models.Model):
    visit_date = models.IntegerField("Время посещения")
    link = models.CharField("Ссылка", max_length=1000)

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"
        ordering = ("-visit_date",)

    def __str__(self):
        return self.link
