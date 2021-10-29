from rest_framework import serializers
from .models import *
from collections import OrderedDict


class PkmnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PkmnModel
        fields = '__all__'

    def to_representation(self, instance):
        base_repr = super().to_representation(instance)

        repr = OrderedDict()
        repr["#"] = base_repr["id"]
        repr["Name"] = base_repr["name"]
        repr["Type 1"] = base_repr["type1"]
        if base_repr["type2"] != None:
            repr["Type 2"] = base_repr["type2"]
        repr["Total"] = base_repr["total"]
        repr["HP"] = base_repr["hp"]
        repr["Attack"] = base_repr["attack"]
        repr["Defense"] = base_repr["defense"]
        repr["Sp. Atk"] = base_repr["sp_atk"]
        repr["Sp. Def"] = base_repr["sp_def"]
        repr["Speed"] = base_repr["speed"]
        repr["Generation"] = base_repr["generation"]
        repr["Legendary"] = base_repr["legendary"]

        return repr
