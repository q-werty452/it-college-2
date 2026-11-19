from django.db import models

from .icons import ICON_CHOICES


class AboutPage(models.Model):
    """Единственная запись: все тексты и заголовки страницы «О нас»."""

    # --- Шапка страницы ---
    hero_title = models.CharField("Заголовок страницы", max_length=120, default="О нас")
    hero_subtitle = models.TextField(
        "Подзаголовок страницы",
        default="IT COLLEGE — место, где будущие программисты, дизайнеры и аналитики получают практические навыки и уверенный старт в профессии.",
    )

    # --- Блок «О колледже» ---
    about_tag = models.CharField("Метка блока", max_length=80, default="О колледже")
    about_title = models.CharField("Заголовок блока", max_length=200, default="Учим тому, что востребовано на рынке")
    about_text = models.TextField(
        "Текст блока",
        default="IT COLLEGE готовит специалистов среднего звена в сфере информационных технологий. Мы выстраиваем обучение вокруг реальных проектов, современных инструментов и тесной связи с работодателями — чтобы выпускник приходил на первое собеседование с готовым портфолио.",
    )

    # --- Карточка справа ---
    badge_text = models.CharField("Бейдж на карточке", max_length=120, default="Диплом государственного образца")
    card_title = models.CharField("Заголовок карточки", max_length=120, default="IT COLLEGE")
    card_text = models.TextField(
        "Текст карточки",
        default="Современное образование в сфере IT — от основ программирования до дизайна и цифровой экономики.",
    )

    # --- Миссия и ценности ---
    values_tag = models.CharField("Ценности: метка", max_length=80, default="Миссия и ценности")
    values_title = models.CharField("Ценности: заголовок", max_length=200, default="Во что мы верим")
    values_subtitle = models.TextField(
        "Ценности: подзаголовок", blank=True,
        default="Принципы, на которых строится вся жизнь колледжа — от учебных планов до общения со студентами.",
    )

    # --- История ---
    history_tag = models.CharField("История: метка", max_length=80, default="История")
    history_title = models.CharField("История: заголовок", max_length=200, default="Наш путь")
    history_subtitle = models.CharField("История: подзаголовок", max_length=255, blank=True, default="Ключевые этапы развития колледжа.")

    # --- Преимущества ---
    adv_tag = models.CharField("Преимущества: метка", max_length=80, default="Преимущества")
    adv_title = models.CharField("Преимущества: заголовок", max_length=200, default="Почему выбирают IT COLLEGE")

    # --- Галерея ---
    gallery_tag = models.CharField("Галерея: метка", max_length=80, default="Галерея")
    gallery_title = models.CharField("Галерея: заголовок", max_length=200, default="Жизнь колледжа")
    gallery_subtitle = models.CharField(
        "Галерея: подзаголовок", max_length=255, blank=True,
        default="Аудитории, мероприятия и студенческие будни в фотографиях.",
    )
    gallery_limit = models.PositiveSmallIntegerField(
        "Сколько фото показывать на странице «О нас»", default=6,
        help_text="Если в галерее больше фото, появится кнопка «Смотреть всю галерею».",
    )

    # --- Команда ---
    team_tag = models.CharField("Команда: метка", max_length=80, default="Команда")
    team_title = models.CharField("Команда: заголовок", max_length=200, default="Люди колледжа")
    team_subtitle = models.TextField(
        "Команда: подзаголовок", blank=True,
        default="Познакомьтесь с теми, кто отвечает за качество обучения, и с нашими выпускниками.",
    )

    # --- Призыв к действию ---
    cta_title = models.CharField("CTA: заголовок", max_length=200, default="Готовы стать частью IT COLLEGE?")
    cta_text = models.TextField(
        "CTA: текст",
        default="Подайте документы онлайн или приходите на день открытых дверей — мы расскажем о программах и ответим на все вопросы.",
    )

    class Meta:
        verbose_name = "Страница «О нас»"
        verbose_name_plural = "Страница «О нас»"

    def __str__(self):
        return "Страница «О нас»"

    def save(self, *args, **kwargs):
        self.pk = 1  # всегда одна запись
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # удалять нельзя

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class OrderedItem(models.Model):
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class AboutFeature(OrderedItem):
    """Пункты списка в блоке «О колледже»."""
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="features")
    icon = models.CharField("Иконка", max_length=30, choices=ICON_CHOICES, default="code")
    title = models.CharField("Заголовок", max_length=150)
    text = models.TextField("Описание")

    class Meta(OrderedItem.Meta):
        verbose_name = "Пункт «О колледже»"
        verbose_name_plural = "Пункты «О колледже»"

    def __str__(self):
        return self.title


class AboutCardStat(OrderedItem):
    """Мини-цифры в карточке справа (2023 / 1500+ / ...)."""
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="card_stats")
    number = models.CharField("Число", max_length=30, help_text="Например: 2023 или 1500+")
    label = models.CharField("Подпись", max_length=100)

    class Meta(OrderedItem.Meta):
        verbose_name = "Цифра в карточке"
        verbose_name_plural = "Цифры в карточке"

    def __str__(self):
        return f"{self.number} — {self.label}"


class AboutCounter(OrderedItem):
    """Анимированные счётчики статистики."""
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="counters")
    icon = models.CharField("Иконка", max_length=30, choices=ICON_CHOICES, default="graduation")
    value = models.PositiveIntegerField("Значение")
    suffix = models.CharField("Суффикс", max_length=10, blank=True, help_text="Например: +")
    label = models.CharField("Подпись", max_length=100)

    class Meta(OrderedItem.Meta):
        verbose_name = "Счётчик статистики"
        verbose_name_plural = "Счётчики статистики"

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


class AboutValue(OrderedItem):
    """Карточки «Миссия и ценности»."""
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="values")
    icon = models.CharField("Иконка", max_length=30, choices=ICON_CHOICES, default="star")
    title = models.CharField("Заголовок", max_length=120)
    text = models.TextField("Описание")

    class Meta(OrderedItem.Meta):
        verbose_name = "Ценность"
        verbose_name_plural = "Ценности"

    def __str__(self):
        return self.title


class AboutMilestone(OrderedItem):
    """Этапы истории."""
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="milestones")
    year = models.CharField("Год", max_length=10)
    title = models.CharField("Заголовок", max_length=150)
    text = models.TextField("Описание")

    class Meta(OrderedItem.Meta):
        verbose_name = "Этап истории"
        verbose_name_plural = "История"

    def __str__(self):
        return f"{self.year} — {self.title}"


class AboutAdvantage(OrderedItem):
    """Преимущества."""
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="advantages")
    icon = models.CharField("Иконка", max_length=30, choices=ICON_CHOICES, default="check")
    title = models.CharField("Заголовок", max_length=120)
    text = models.CharField("Описание", max_length=255)

    class Meta(OrderedItem.Meta):
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.title


class AboutLinkCard(OrderedItem):
    """Карточки-ссылки в блоке «Команда»."""
    URL_CHOICES = [
        ("director-url", "Директор"),
        ("sotrudniki-url", "Сотрудники"),
        ("graduates-url", "Выпускники"),
        ("spec-url", "Специальности"),
        ("open-day-url", "День открытых дверей"),
        ("submit-document-url", "Подать документы"),
        ("gallery-url", "Галерея"),
    ]
    page = models.ForeignKey(AboutPage, on_delete=models.CASCADE, related_name="link_cards")
    icon = models.CharField("Иконка", max_length=30, choices=ICON_CHOICES, default="user")
    title = models.CharField("Заголовок", max_length=100)
    text = models.CharField("Описание", max_length=255)
    url_name = models.CharField("Куда ведёт", max_length=60, choices=URL_CHOICES)

    class Meta(OrderedItem.Meta):
        verbose_name = "Карточка-ссылка"
        verbose_name_plural = "Карточки-ссылки (Команда)"

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    """Фото галереи. Размер плитки выбирается в админке."""
    SIZE_CHOICES = [
        ("auto", "Авто (по шаблону)"),
        ("normal", "Обычная (1×1)"),
        ("wide", "Широкая (2×1)"),
        ("tall", "Высокая (1×2)"),
        ("big", "Большая (2×2)"),
    ]
    image = models.ImageField("Фото", upload_to="gallery/%Y/%m/")
    title = models.CharField("Подпись", max_length=150, blank=True)
    size = models.CharField("Размер плитки", max_length=10, choices=SIZE_CHOICES, default="auto")
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Показывать", default=True)
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Фото галереи"
        verbose_name_plural = "Галерея колледжа"

    def __str__(self):
        return self.title or f"Фото #{self.pk}"
