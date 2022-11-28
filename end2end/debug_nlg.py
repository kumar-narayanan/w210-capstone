import uuid
import json
import requests

from predictOnline import get_args,get_device, load_model, load_tokenizer, predictNLU

pred_config = {"model_dir":"./train/meta", "batch_size":32, "no_cuda":False }
args = get_args(pred_config)
device = get_device(pred_config)
model = load_model(pred_config, args, device)
tokenizer = load_tokenizer(args)

#workflow = {
#        "clinic_find": ["name", "location", "book_day", "book_time", "book_people", "vaccination_type"],
#        "clinic_book": ["name", "location", "book_day", "book_time", "book_people", "vaccination_type"],
#        "restaurant_book" : ["name", "location", "book_day", "book_time", "book_people"],
#        "hotel_book" : ["name", "location", "book_day", "book_rooms", "creditcard", "consent_to_charge"]
#}

workflow = {
        "clinic_find": ["name", "location", "bookday", "bookpeople"],
        "clinic_book": ["vaccinebrand", "bookday", "booktime", "bookpeople", "customername", "customer_phonenumber"],
        "restaurant_book" : ["name", "location", "bookday", "booktime", "bookpeople"],
        "hotel_book" : ["name", "location", "bookday", "book_rooms", "creditcard", "consent_to_charge"]
        }

state_tracker = {};
db = {"dublin_pfizer_11_11_22": "8,9,10,11", "paloalto_moderna_11_21_22": "8,9,10,11"}

#prompts = {
#        "name": "Hi, How are you? I am Chatbot. May I know your name please",
#        "location": "What is your location",
#        "book_day": "Could you tell us the day you want to book the service for",
#        "book_people": "How many people need the service",
#        "book_adults": "How many adults and kids",
#        "book_kids": "How many kids",
#        "vaccination_type": "What vaccination do you want",
#        "ref_num": "here is your ref number for your appointment 42FG3W",
#        "thanks": "Thank you for calling us. Have a great day"
#}

prompts = {
        "welcome": "Hi, How are you? welcome to CAiFE. how may I help you today?",
        "customername": "May I know your name please",
        "customer_phonenumber": "your phone number as well.",
        "location": "Which part of the town would you prefer: centre, east, north, south, west?",
        "bookday": "which day you want to book the appointment for",
        "bookpeople": "How many people need the service",
        "type": "what type of service you are seeking: flu or covid",
        "booktime": "what time would you prefer for the appointment",
        "vaccinebrand": "which of the vaccines do you prefer: pfizer, moderna, novaform",
        "reference_number": "here is reference number for your appointment 42FG3W",
        "thanks": "Thank you for using CAiFE. Have a great day",
        "name": "May I have your name please"
}

class EntityState:
    _id = ""
    domain = ""
    name = ""
    location = ""
    area = ""
    customername = ""
    customer_phonenumber = ""
    vaccinebrand = ""
    bookday = ""
    booktime = ""
    bookpeople = -1
    book_adults = -1
    book_kids = -1
    book_rooms = -1
    creditcard = ""
    consent_to_charge = ""
    reference_number = ""

    def __init__(self, _id, domain):
        self._id = _id
        self.domain = domain

    def get_domain(self):
        return self.domain

    def set_name(self, n):
        self.name = n

    def set_location(self, location):
        self.location = location

    def set_area(self, area):
        self.area = area

    def set_vaccinebrand(self, vb):
        self.vaccinebrand = vb

    def set_customername(self, cn):
        self.customername = cn

    def set_customer_phonenumber(self, cphone):
        self.customer_phonenumber = cphone

    def set_bookday(self, n):
        self.bookday = n

    def set_booktime(self, n):
        self.booktime = n

    def set_bookpeople(self, n):
        self.bookpeople = n

    def set_book_adults(self, n):
        self.book_adults = n

    def set_book_kids(self, n):
        self.book_kids = n

    def set_book_rooms(self, n):
        self.book_rooms = n

    def set_creditcard(self, n):
        self.creditcard = n

    def set_consent_to_charge(self, n):
        self.consent_to_charge = n

    def set_reference_number(self, n):
        self.reference_number = n

    def get_reference_number(self):
        return self.reference_number

    def is_fieldvalue_present(self, n):
        if n == "name":
            if (len(self.name) == 0):
                return False
            else:
                return True
        elif n == "area":
            if (len(self.area) == 0):
                return False
            else:
                return True
        elif n == "vaccinebrand":
            if (len(self.vaccinebrand) == 0):
                return False
            else:
                return True
        elif n == "location":
            if (len(self.location) == 0):
                return False
            else:
                return True
        elif n == "customername":
            if (len(self.customername) == 0):
                return False
            else:
                return True
        elif n == "customer_phonenumber":
            if (len(self.customer_phonenumber) == 0):
                return False
            else:
                return True
        elif n == "bookday":
            if (len(self.bookday) == 0):
                return False
            else:
                return True
        elif n == "booktime":
            if (len(self.booktime) == 0):
                return False
            else:
                return True
        elif n == "bookpeople":
            if self.bookpeople > 0:
                return True
            else:
                return False
        elif n == "book_adults":
            if self.book_adults > 0:
                return True
            else:
                return False
        elif n == "book_kids":
            if self.book_kids > 0:
                return True
            else:
                return False
        elif n == "book_rooms":
            if self.book_rooms > 0:
                return True
            else:
                return False
        elif n == "creditcard":
            if (len(self.creditcard) == 0):
                return False
            else:
                return True
        elif n == "consent_to_charge":
            if len(self.consent_to_charge) == 0:
                return False
            else:
                return True

    def print_(self):
        print("domain:", self.domain)
        print("name:", self.name)
        print("address:", self.location)
        print("vaccinebrand:", self.vaccinebrand)
        print("bookday:", self.bookday)
        print("booktime:", self.booktime)
        print("bookpeople:", self.bookpeople)
        print("book_kids:", self.book_kids)
        print("book_rooms:", self.book_room)
        print("creditcard:", self.creditcard)
        print("consent_to_charge:", self.consent_to_charge)
        print("reference_number:", self.reference_number)
        print("area", self.area)
        print("customername", self.customername)
        print("customer_phonenumber", self.customer_phonenumber )

def update_slots(data, person):
    if data.get('slots') is not None:
        slots = data.get('slots')
        if "name" in slots:
            person.set_name(slots["name"])
        if "location" in slots:
            person.set_location(slots["location"])
        if "bookday" in slots:
            person.set_bookday(slots["bookday"])
        if "booktime" in slots:
            person.set_booktime(slots["booktime"])
        if "bookpeople" in slots:
            person.set_bookpeople(slots["bookpeople"])
        if "book_adults" in slots:
            person.set_book_adults(slots["book_adults"])
        if "book_kids" in slots:
            person.set_book_kids(slots["book_kids"])
        if "vaccinebrand" in slots:
            person.set_vaccinebrand(slots["vaccinebrand"])
        if "book_rooms" in slots:
            person.set_book_rooms(slots["book_rooms"])
        if "creditcard" in slots:
            person.set_creditcard(slots["creditcard"])
        if "consent_to_charge" in slots:
            person.set_creditcard(slots["consent_to_charge"])
        if "customername" in slots:
            person.set_customername(slots["customername"])
        if "customer_phonenumber" in slots:
            person.set_customer_phonenumber(slots["customer_phonenumber"])

def find_first_missing(person):
    w = workflow[person.get_domain()]
    for x in w:
        if person.is_fieldvalue_present(x):
            continue
        else:
            return x
    return ""

def get_prompt(k):
    return prompts[k]

#uuid
def call_db(person):
    person.set_ref_num("42FG3W")
    return prompts['reference_number']

with open('utterance.txt', 'r') as fp:
    utterances = fp.readlines()
    
for utterance in utterances:
    utterance = utterance.strip()
    msg_json = '{"message": ' + '"' + utterance + '"'  + ',' + '"id":"123456"}'
    incoming_data = json.loads(msg_json)
    nlu_resp = predictNLU(incoming_data.get('message'), pred_config, args, device, model, tokenizer)
    print("utterance:", utterance)
    print("nlu_resp:", nlu_resp)

    data =json.loads(nlu_resp)
    #print("data:", data)
    if incoming_data.get('id') not in state_tracker.keys():
        domain = data.get('domain') + '_' + data.get('intent')
        state_tracker[incoming_data.get('id')] = EntityState(incoming_data.get('id'), domain)

    person = state_tracker[incoming_data.get('id')]
    update_slots(data, person)

    missing_field = find_first_missing(person)

    chat_resp = ""
    if len(missing_field) > 0:
        chat_resp = get_prompt(missing_field)
    elif len(person.get_ref_num()) == 0:
        chat_resp = call_db(person)
    else:
        chat_resp = get_prompt("thanks")

    print("chat_resp:", chat_resp)
