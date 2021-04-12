from django.db import models

from ..choices import PHQ_CHOICES


class PHQ9ModelMixin(models.Model):

    ph9interst = models.CharField(
        verbose_name="Little interest or pleasure in doing things",
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9feel = models.CharField(
        verbose_name="Feeling down, depressed or hopeless",
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9troubl = models.CharField(
        verbose_name="Trouble falling/staying asleep, sleeping too much",
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9tired = models.CharField(
        verbose_name="Feeling tired or having little energy",
        max_length=15,
        choices=PHQ_CHOICES,
    )
    ph9appetit = models.CharField(
        verbose_name="Poor appetite or over eating",
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9badabt = models.CharField(
        verbose_name=(
            "Feeling bad about yourself or that you are a "
            "failure or have let yourself or your family down"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9concen = models.CharField(
        verbose_name=(
            "Trouble concentrating on things such as reading the "
            "newspapers or watching television"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9moving = models.CharField(
        verbose_name=(
            "Moving or speaking so slowly  that other people could have "
            "noticed or the opposite: being so fidgety or restless that "
            "you have been moving around a lot more than usual"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9though = models.CharField(
        verbose_name=(
            "Thoughts that you would be better off dead or of hurting yourself in some way"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
    )

    ph9functio = models.CharField(
        verbose_name=(
            "If you checked off any problems on this questionnaire so far, "
            "how difficult have these problems made it for you to do your "
            "work, take care of things at home or get along with other people?"
        ),
        max_length=15,
        choices=PHQ_CHOICES,
    )

    class Meta:
        abstract = True
        verbose_name = "Patient Health Questionnaire-9 (PHQ-9)"
        verbose_name_plural = "Patient Health Questionnaires-9 (PHQ-9)"
