from django.db import models

LANGUAGES = [
    ("ESP","Spanish"),
    ("ENG","English"),
    ("GER","German"),
    ("FRC","French"),
    ("CHI","Chinese"),
    ("ITA","Italian"),
    ("JAP","Japanese"),
    ("ARB","Arabic"),
]

class Languages(models.Model):
    """
        @notice Each language represnts languages that user speaks
        @notice level should be >= 100
    """
    name = models.CharField(choices=LANGUAGES, max_length=3)
    level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + self.level


class Interest(models.Model):
    """
        @notice Interest show what are the preferences of the user
    """
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=15,blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """
        @notice Location show where users are currently located
    """
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(blank=False,max_digits=25,decimal_places=15)
    longitude = models.DecimalField(blank=False,max_digits=25,decimal_places=15)

    def __str__(self):
        return self.name
