from django.db import models

class Crop_Parameters(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    dx = models.IntegerField()
    dy = models.IntegerField()

    def __str__(self):
        return self.x, self.dx, self.y, self.dy

class Binarize_Parameters(models.Model):
    b = models.IntegerField()
    g = models.IntegerField()
    r = models.IntegerField()
    k = models.IntegerField()
    
    def __str__(self):
        return self.b, self.g, self.r, self.k