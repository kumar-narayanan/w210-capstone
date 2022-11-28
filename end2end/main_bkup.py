from flask import Flask, render_template
from flask_socketio import SocketIO
import uuid
import json
import requests

from predictOnline import get_args,get_device, load_model, load_tokenizer, predictNLU

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")

pred_config = {"model_dir":"./train/hotel", "batch_size":32, "no_cuda":False }
args = get_args(pred_config)
device = get_device(pred_config)
model = load_model(pred_config, args, device)
tokenizer = load_tokenizer(args)


workflow = {
        "clinic_find": ["name", "location", "book_day", "book_time", "book_people", "vaccination_type"],
        "clinic_book": ["name", "location", "book_day", "book_time", "book_people", "vaccination_type"],
        "restaurant_book" : ["name", "location", "book_day", "book_time", "book_people"],
        "hotel_book" : ["name", "location", "book_day", "book_rooms", "creditcard", "consent_to_charge"]
}


#write to flat file
state_tracker = {};
db = {"dublin_pfizer_11_11_22": "8,9,10,11", "paloalto_moderna_11_21_22": "8,9,10,11"}

class EntityState:
    _id = ""
    domain = ""
    name = ""
    location = ""
    vaccination_type = ""
    book_day = ""
    book_time = ""
    book_people = -1
    book_adults = -1
    book_kids = -1
    book_rooms = -1
    creditcard = ""
    consent_to_charge = ""
    ref_num = ""

    def __init__(self, _id, domain):
        self._id = _id
        self.domain = domain

    def get_domain(self):
        return self.domain

    def set_name(self, n):
        self.name = n

    def set_location(self, location):
        self.location = location

    def set_vaccination_type(self, vt):
        self.vaccination_type = vt

    def set_book_day(self, n):
        self.book_day = n

    def set_book_time(self, n):
        self.book_time = n

    def set_book_people(self, n):
        self.book_people = n

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

    def set_ref_num(self, n):
        self.ref_num = n

    def get_ref_num(self):
        return self.ref_num

    def is_fieldvalue_present(self, n):
        if n == "name":
            if (len(self.name) == 0):
                return False
            else:
                return True

        elif n == "location":
            if (len(self.location) == 0):
                return False
            else:
                return True
        elif n == "vaccination_type":
            if (len(self.vaccination_type) == 0):
                return False
            else:
                return True
        elif n == "book_day":
            if (len(self.book_day) == 0):
                return False
            else:
                return True
        elif n == "book_time":
            if (len(self.book_time) == 0):
                return False
            else:
                return True
        elif n == "book_people":
            if self.book_people > 0:
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
        print("vaccination_type:", self.vaccination_type)
        print("book_day:", self.book_day)
        print("book_time:", self.book_time)
        print("book_people:", self.book_people)
        print("book_people:", self.book_kids)
        print("book_rooms:", self.book_room)
        print("creditcard:", self.creditcard)
        print("consent_to_charge:", self.consent_to_charge)
        print("ref_num:", self.ref_num)


def update_slots(data, person):
    if data.get('slots') is not None:
        slots = data.get('slots')
        if "name" in slots:
            person.set_name(slots["name"])
        if "location" in slots:
            person.set_location(slots["location"])
        if "book_day" in slots:
            person.set_book_day(slots["book_day"])
        if "book_time" in slots:
            person.set_book_time(slots["book_time"])
        if "book_people" in slots:
            person.set_book_people(slots["book_people"])
        if "book_adults" in slots:
            person.set_book_adults(slots["book_adults"])
        if "book_kids" in slots:
            person.set_book_kids(slots["book_kids"])
        if "vaccination_type" in slots:
            person.set_vaccination_type(slots["vaccination_type"])
        if "book_rooms" in slots:
            person.set_book_rooms(slots["book_rooms"])
        if "creditcard" in slots:
            person.set_creditcard(slots["creditcard"])
        if "consent_to_charge" in slots:
            person.set_creditcard(slots["consent_to_charge"])

def find_first_missing(person):
    w = workflow[person.get_domain()]
    for x in w:
        if person.is_fieldvalue_present(x):
            continue
        else:
            return x
    return ""


prompts = {
        "name": "Hi, How are you? I am Chatbot. May I know your name please",
	"location": "What is your location",
	"book_day": "Could you tell us the day you want to book the service for",
	"book_people": "How many people need the service",
	"book_adults": "How many adults and kids",
	"book_kids": "How many kids",
	"vaccination_type": "What vaccination do you want",
	"ref_num": "here is your ref number for your appointment 42FG3W",
	"thanks": "Thank you for calling us. Have a great day"
}


def get_prompt(k):
    return prompts[k]

#uuid
def call_db(person):
    person.set_ref_num("27JR6F")
    return prompts['ref_num']


@socketio.on('message')
def handle_message(msg_json):
    incoming_data = json.loads(msg_json)
    print('received my event: ' + incoming_data.get('message'))
    print('received my event: ' + str(incoming_data.get('id')))
    # NLU
    #nlu_url = "https://xt45bovwxa.execute-api.us-west-2.amazonaws.com/Prod/sm-api"
    #nlu_params = {'message': incoming_data.get('message')}
    #nlu_resp = requests.get(url = nlu_url, params = nlu_params)
    nlu_resp = predictNLU(incoming_data.get('message'), pred_config, args, device, model, tokenizer)
    # NLG
    
    data =json.loads(nlu_resp)
    print("nlu response")
    print(data)
    if incoming_data.get('id') not in state_tracker.keys():
        domain = data.get('domain') + '_' + data.get('intent')
        state_tracker[incoming_data.get('id')] = EntityState(incoming_data.get('id'), domain)

    person = state_tracker[incoming_data.get('id')]
    update_slots(data, person)

    missing_field = find_first_missing(person)

    chat_resp = ""
    #if the user persist with wrong message...add some "sorry i could not understand"
    if len(missing_field) > 0:
        chat_resp = get_prompt(missing_field)
    elif len(person.get_ref_num()) == 0:
        chat_resp = call_db(person)
    else:
        chat_resp = get_prompt("thanks")
    print("chat_resp")
    print(chat_resp)
    socketio.emit('response_chat', chat_resp)

@socketio.on('connect')
def test_connect():
    print('connected with a client')

@app.route('/medinova')
def chat_medinova():
    print('in medinova')
    return render_template('/home/ubuntu/caife/templates/clinic/index.html')
 #   return render_template('clinic/index.html')


@app.route('/caife')
def chat():
    print('in caife')
    return render_template('caife/index.html')

@app.route('/')
def sessions():
    print('here in the root ')
    return render_template('session.html')

if __name__ == '__main__':
    socketio.run(app, host="172.31.86.221",port=5000)
