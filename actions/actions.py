# This files contains your custom actions which can be used to run
# custom Python code.


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import FormValidation, SlotSet, EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from algoliasearch.search_client import SearchClient

client = SearchClient.create('BQCT474121', 'b72f4c8a6b93d0afc8221d06c66e1e66')
index = client.init_index('dev_clothes_v2')

ALLOWED_COLORS_GIRLS = ['morado', 'amarillo', 'negro',
                        'rosado', 'celeste', 'rojo', 'palo de rosa']
ALLOWED_CLOTHES_GIRLS = ['pantalones', 'blusas', 'todos']
ALLOWED_COLORS_BOYS = ['rojo', 'azul', 'beige', 'blanco']
ALLOWED_CLOTHES_BOYS = ['busos', 'camisetas', 'todos']
ALLOWED_GENDERS = ['niños', 'niño', 'niñas', 'niña']


class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class ValidateClothesPriceForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_clothes_price_form"

    @staticmethod
    def change_name_button(option: str) -> List:
        """Add new button"""

        new_button = 'Ver Todo' if option == 'todos' else option
        return new_button.capitalize()

    @staticmethod
    def is_int(string: Any) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_gender(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `gender` value."""

        if slot_value.lower() not in ALLOWED_GENDERS:
            dispatcher.utter_message(response="utter_ask_gender")
            return {"gender": None}
        else:
            return {"gender": slot_value}
    
    def validate_comparator(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `comparator` value."""

        if type(slot_value) is str:
            return {"comparator": slot_value}
        else:
            print('compa', slot_value)
            return {"comparator": slot_value[0]}
            

    def validate_price(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `comparator` value."""

        if slot_value >= 3 and slot_value <= 20:
            return {"price": slot_value}
        else:
            dispatcher.utter_message(
                    text=f"El valor ingresado es inválido. Tenemos ropa desde $3 a $20 dólares 💰.")
            return {"price": None}



class ValidateClothesForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_clothes_form"

    @staticmethod
    def change_name_button(option: str) -> List:
        """Add new button"""

        new_button = 'Ver Todo' if option == 'todos' else option
        return new_button.capitalize()

    @staticmethod
    def is_int(string: Any) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_gender(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `gender` value."""

        if slot_value.lower() not in ALLOWED_GENDERS:
            dispatcher.utter_message(response="utter_ask_gender")
            return {"gender": None}
        else:
            return {"gender": slot_value}

    def validate_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `color` value."""

        gender = tracker.get_slot("gender")

        intent_name = tracker.latest_message["intent"]["name"]
        if intent_name == 'deny':
            return {"color": 'no'}

        if gender == 'niña':
            if slot_value.lower() not in ALLOWED_COLORS_GIRLS:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores como: \n- Morado\n- Amarillo\n- Negro\n- Rosado\n- Celeste\n- Rojo\n- Palo de Rosa")
                return {"color": None}
            else:
                return {"color": slot_value}

        if gender == 'niño':
            if slot_value.lower() not in ALLOWED_COLORS_BOYS:
                dispatcher.utter_message(
                    text=f"Por el momento disponemos de colores como: \n- Rojo\n- Azul\n- Beige\n- Blanco")
                return {"color": None}
            else:
                return {"color": slot_value}

    def validate_category(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `category` value."""
        gender = tracker.get_slot("gender")
        print('category', slot_value)

        if gender == 'niña':
            if slot_value.lower() not in ALLOWED_CLOTHES_GIRLS:
                buttons = [{"title": self.change_name_button(
                    p), "payload": p} for p in ALLOWED_CLOTHES_GIRLS]
                dispatcher.utter_message(text=f"Te cuento que contamos con los siguientes tipos de ropa para niñas:",
                                         buttons=buttons)
                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}

        if gender == 'niño':
            if slot_value.lower() not in ALLOWED_CLOTHES_BOYS:
                buttons = [{"title": self.change_name_button(
                    p), "payload": p} for p in ALLOWED_CLOTHES_BOYS]
                dispatcher.utter_message(text=f"Te cuento que contamos con los siguientes tipos de ropa para niños:",
                                         buttons=buttons)
                return {"category": None}
            else:
                dispatcher.utter_message(text=f"Excelente elección 👍🏻")
                return {"category": slot_value}

    def validate_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `size` value."""

        if self.is_int(slot_value) and (int(slot_value) >= 1 and int(slot_value)  <= 5):
            return {"size": slot_value}
        else:
            gender = tracker.get_slot("gender")
            if gender == 'niña':
                dispatcher.utter_message(
                    text=f"Lo siento 😭, para esa edad no disponemos. Te cuento que tenemos ropa para niñas de 1 a 5 años:")
                return {"size": None}
            if gender == 'niño':
                dispatcher.utter_message(
                    text=f"Lo siento 😭, para esa edad no disponemos. Te cuento que tenemos ropa para niños de 1 a 5 años:")
                return {"size": None}


class AskForCategoryAction(Action):

    @staticmethod
    def change_name_button(option: str) -> List:
        """Add new button"""

        new_button = 'Ver Todo' if option == 'todos' else option
        return new_button.capitalize()

    def name(self) -> Text:
        return "action_ask_category"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
            ) -> List[EventType]:

        gender = tracker.get_slot("gender")

        if gender == 'niña':
            buttons = [{"title": self.change_name_button(
                p), "payload": p} for p in ALLOWED_CLOTHES_GIRLS]
            dispatcher.utter_message(
                text=f"Te cuento que contamos con los siguientes tipos de ropa para niñas 👧🏻:", buttons=buttons)
        else:
            buttons = [{"title": self.change_name_button(
                p), "payload": p} for p in ALLOWED_CLOTHES_BOYS]

            dispatcher.utter_message(
                text=f"Te cuento que contamos con los siguientes tipos de ropa para niños 👦🏻:", buttons=buttons)

        return []


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get slots and save as tuple
        parameters = [tracker.get_slot("gender"), tracker.get_slot(
            "size"), tracker.get_slot("category"), tracker.get_slot("color")]

        if parameters[0] == 'niño':
            parameters[0] = 'M'
        else:
            parameters[0] = 'F'

        print(parameters)

        if parameters[2] != 'todos':

            if parameters[3] == 'no':
                objects = index.search("", {
                    "facetFilters": [
                        [
                            "gender:{0[0]}".format(parameters)
                        ],
                        [
                            "age:{0[1]}".format(parameters)
                        ],
                        [
                            "category:{0[2]}".format(parameters)
                        ],
                    ]
                })
            else:
                objects = index.search("", {
                    "facetFilters": [
                        [
                            "gender:{0[0]}".format(parameters)
                        ],
                        [
                            "age:{0[1]}".format(parameters)
                        ],
                        [
                            "category:{0[2]}".format(parameters)
                        ],
                        [
                            "color:{0[3]}".format(parameters)
                        ],
                    ]
                })
        else:

            if parameters[3] == 'no':
                objects = index.search("", {
                    "facetFilters": [
                        [
                            "gender:{0[0]}".format(parameters)
                        ],
                        [
                            "age:{0[1]}".format(parameters)
                        ],
                    ]
                })
            else:
                objects = index.search("", {
                    "facetFilters": [
                        [
                            "gender:{0[0]}".format(parameters)
                        ],
                        [
                            "age:{0[1]}".format(parameters)
                        ],
                        [
                            "color:{0[3]}".format(parameters)
                        ],
                    ]
                })


        clothes = objects['hits']

        product = []
        for x in clothes:
            print(x['name'])
            product.append({'title': x['name'], 'subtitle': "{0}\nStock: {1} disponibles \nPrecio: ${2}".format(x['material'], x['quantity'], x['price']), "image_url": x['image'], "buttons": [
                {
                    "title": "Comprar",
                    "url": "https://www.instagram.com/creacionesjasmina/",
                    "type": "web_url"
                }
            ]})

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": product
                }
            }
        }

        if clothes:
            dispatcher.utter_message(json_message=message)

            slots_to_reset = ["gender", "size", "color", "category"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            text = (
                f"No disponemos de ese producto en específico. Pero puedes seguir buscando..."
            )
            dispatcher.utter_message(text=text)

            slots_to_reset = ["gender", "size", "color", "category"]
            return [SlotSet(slot, None) for slot in slots_to_reset]


class ActionProductPriceSearch(Action):
    def name(self) -> Text:
        return "action_product_price_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # get slots and save as tuple
        parameters = [tracker.get_slot("gender"), tracker.get_slot(
            "price"), tracker.get_slot("comparator")]

        if parameters[0] == 'niño':
            parameters[0] = 'M'
        else:
            parameters[0] = 'F'

        print(parameters)

        if parameters[2] == 'menor':
            objects = index.search("", {
                "numericFilters": [
                    "price<={0[1]}".format(parameters)
                ],
                "facetFilters": [
                    [
                        "gender:{0[0]}".format(parameters)
                    ],
                ]
            })
        else:
            objects = index.search("", {
                "numericFilters": [
                    "price>{0[1]}".format(parameters)
                ],
                "facetFilters": [
                    [
                        "gender:{0[0]}".format(parameters)
                    ],
                ]
            })

        clothes = objects['hits']

        product = []
        for x in clothes:
            print(x['name'])
            product.append({'title': x['name'], 'subtitle': "{0}\nStock: {1} disponibles \nPrecio: ${2}".format(x['material'], x['quantity'], x['price']), "image_url": x['image'], "buttons": [
                {
                    "title": "Comprar",
                    "url": "https://www.instagram.com/creacionesjasmina/",
                    "type": "web_url"
                }
            ]})

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": product
                }
            }
        }

        if clothes:
            dispatcher.utter_message(json_message=message)

            slots_to_reset = ["gender", "price", "comparator", "size"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            text = (
                f"No disponemos de ese producto en específico. Pero puedes seguir buscando..."
            )
            dispatcher.utter_message(text=text)

            slots_to_reset = ["gender", "price", "comparator", "size"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
