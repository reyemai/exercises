import json

import requests


class PokemonApi(object):
    def __init__(self, host=r"http://127.0.0.1:8000"):
        object.__init__(self)
        self.host = host
        self.base_url = "/".join([host, "pokemon"])

    def _get_request(self, data={}):
        try:
            response = requests.get(self.base_url, data)
        except Exception as e:
            print("Could not connect to " + str(self.host))
            return {}
        response_as_dict = json.loads(response.content)
        return response_as_dict

    def get_request(self, data={}):
        return self._get_request(data).get("result", [])

    def get_all_pkmn(self):
        return self.get_request()

    def get_pkmn_by_type(self, type):
        return self.get_request({"type": type})

    def get_pkmn_by_name(self, name):
        pkmns = self.get_request({"name": name})
        if len(pkmns) == 1:
            return pkmns[0]
        else:
            return None

    def get_pkmn_by_name_similarity(self, name):
        pkmns = self.get_request({"search": name,"page":1})
        if len(pkmns) > 0:
            return pkmns[0]
        else:
            return None


def preview(pkmns):
    s = "\t" + "\n\t".join([p.get("Name") for p in pkmns[:10]])
    if len(pkmns) > 10:
        s += "\n\t... And other " + str(len(pkmns) - 10)
    print(s)


def main():
    pkmnApi = PokemonApi()

    print("\nGet all pkmn...")
    pkmns = pkmnApi.get_all_pkmn()
    print(" - got " + str(len(pkmns)) + " pkmns:")
    preview(pkmns)

    print("\nGet pkmn of type 'Ghost'...")
    pkmns = pkmnApi.get_pkmn_by_type("Ghost")
    print(" - got " + str(len(pkmns)) + " pkmns.")
    preview(pkmns)

    print("\nGet pkmn of type 'Grass'...")
    pkmns = pkmnApi.get_pkmn_by_type("Grass")
    print(" - got " + str(len(pkmns)) + " pkmns:")
    preview(pkmns)

    print("\nGet pkmn with Attack>=170...")
    pkmns = pkmnApi.get_request({"attack[gte]": 170})
    print(" - got " + str(len(pkmns)) + " pkmns:")
    preview(pkmns)

    print("\nGet pkmns page by page for hp>130...")
    response = pkmnApi._get_request({"page": 1, "hp[gt]": 130})
    num_pages = response.get("num_pages", 1)
    pkmns = response.get("result")
    print("Page 1/" + str(num_pages) + ":")
    preview(pkmns)
    for i in range(2, num_pages + 1):
        response = pkmnApi._get_request({"page": i, "hp[gt]": 130})
        pkmns = response.get("result")
        print("Page " + str(i) + "/" + str(num_pages) + ":")
        preview(pkmns)

    print("\nGet Oddish...")
    pkmn = pkmnApi.get_pkmn_by_name("Oddish")
    print(" - got " + pkmn.get("Name") + " !")

    print("\nGet most similar to 'Marco' based on Levenshtein...")
    pkmn = pkmnApi.get_pkmn_by_name_similarity("Marco")
    print(" - got " + pkmn.get("Name") + " !")


if __name__ == "__main__":
    main()
