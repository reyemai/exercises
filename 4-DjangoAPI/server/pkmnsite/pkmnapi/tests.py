import json
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .pkmn import PkmnDict


class PkmnModelTests(TestCase):
    def _get_json_file(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",
                            "..", "..", "Data", "pokemon.json")

    def load_file(self):
        json_path = self._get_json_file()
        data = None
        with open(json_path, "rb") as f:
            data = f.read()

        json_file = SimpleUploadedFile(json_path,
                                       data,
                                       content_type="application/json")
        return self.client.post('/load/', {'file': json_file})

    def test_load_json(self):

        json_path = self._get_json_file()
        if os.path.isfile(json_path):
            data = None
            with open(json_path, encoding="utf-8") as f:
                data = f.read()

            pkmn_list1 = json.loads(data)
            pkmn_list2 = PkmnDict.parse(data)

            self.assertEquals(len(pkmn_list1), len(pkmn_list2))

    def test_api_response(self):
        response = self.client.get('/pokemon/')
        self.assertEquals(response.status_code, 200)
        values = json.loads(response.content)

        self.load_file()

        response = self.client.get('/pokemon/')
        self.assertEquals(response.status_code, 200)
        values = json.loads(response.content)
        self.assertEquals(values["count"], 643)

    def test_total_response(self):
        self.load_file()

        response = self.client.get('/pokemon/')
        self.assertEquals(response.status_code, 200)
        pkmns = json.loads(response.content)

        for p in pkmns["result"]:
            total = 0
            total += p.get("HP")
            total += p.get("Attack")
            total += p.get("Defense")
            total += p.get("Sp. Atk")
            total += p.get("Sp. Def")
            total += p.get("Speed")
            self.assertEquals(total, p.get("Total"))

    def test_no_ghost_legendary(self):
        self.load_file()

        response = self.client.get('/pokemon/')
        self.assertEquals(response.status_code, 200)
        pkmns = json.loads(response.content)

        for p in pkmns["result"]:
            types = []
            types.append(p["Type 1"])
            if p.get("Type 2", None) != None:
                types.append(p.get("Type 2", None))

            self.assertTrue("Ghost" not in types)
            self.assertTrue(not p["Legendary"])
