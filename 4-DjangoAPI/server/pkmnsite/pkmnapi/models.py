from django.db import models
from computed_property import ComputedIntegerField


class PkmnModel(models.Model):

    id = models.IntegerField(primary_key=True)  # "#": 347
    name = models.CharField(max_length=200)  # "Name": "Anorith"
    type1 = models.CharField(max_length=50)  # "Type 1": "Rock"
    type2 = models.CharField(max_length=50, null=True,
                             default=None)  # "Type 2": "Rock"
    total = ComputedIntegerField('compute_total')  # "Total": 355
    hp = models.IntegerField()  # "HP": 45
    attack = models.IntegerField()  # "Attack": 95
    defense = models.IntegerField()  # "Defense": 50
    sp_atk = models.IntegerField()  # "Sp. Atk": 40
    sp_def = models.IntegerField()  # "Sp. Def": 50
    speed = models.IntegerField()  # "Speed": 75
    generation = models.IntegerField()  # "Generation": 3
    legendary = models.BooleanField(default=False)  # "Legendary": false

    def __str__(self):
        return self.name

    @property
    def compute_total(self):
        total = 0
        total += self.hp
        total += self.attack
        total += self.defense
        total += self.sp_atk
        total += self.sp_def
        total += self.speed
        return total
