from dialogue_flow import DialogueFlow, HIGHSCORE, LOWSCORE
from datetime import datetime
from data import names

component = DialogueFlow('prestart')

standard_opening = "Hi this is an Alexa Prize Socialbot."

arcs = []

arcs.extend([(x, 'names', 'type') for x in names])
arcs.extend([])
for arc in arcs:
    component.knowledge_base().add(*arc)

def check_launch_request(arg_dict):
    if arg_dict:
        if arg_dict["request_type"] == "LaunchRequest":
            return HIGHSCORE, {}
    return 0, {}

def check_new(arg_dict):
    if arg_dict:
        if "prev_conv_date" not in arg_dict or arg_dict["prev_conv_date"] is None:
            return HIGHSCORE, {}
    return 0, {}

def check_infreq(arg_dict):
    if arg_dict:
        if "prev_conv_date" in arg_dict and arg_dict["prev_conv_date"] is not None:
            old_datetime = datetime.strptime(arg_dict["prev_conv_date"], '%Y-%m-%d %H:%M:%S.%f')
            delta = datetime.today() - old_datetime
            if delta.days >= 7:
                return HIGHSCORE, {}
    return 0, {}

def check_freq(arg_dict):
    if arg_dict:
        if "prev_conv_date" in arg_dict and arg_dict["prev_conv_date"] is not None:
            old_datetime = datetime.strptime(arg_dict["prev_conv_date"], '%Y-%m-%d %H:%M:%S.%f')
            delta = datetime.today() - old_datetime
            if delta.days < 7:
                return HIGHSCORE, {}
    return 0, {}

def is_new_user(arg_dict, score, vars):
    score, vars = check_launch_request(arg_dict)
    if score == HIGHSCORE:
        score, vars = check_new(arg_dict)
        if score == HIGHSCORE:
            return HIGHSCORE, {}
    return 0, {}

def is_infreq_user(arg_dict, score, vars):
    score, vars = check_launch_request(arg_dict)
    if score == HIGHSCORE:
        score, vars = check_infreq(arg_dict)
        if score == HIGHSCORE:
            return HIGHSCORE, {}
    return 0, {}

def is_freq_user(arg_dict, score, vars):
    score, vars = check_launch_request(arg_dict)
    if score == HIGHSCORE:
        score, vars = check_freq(arg_dict)
        if score == HIGHSCORE:
            return HIGHSCORE, {}
    return 0, {}


# pre start
component.add_transition(
    'prestart', 'prestart', None, {'x'}, settings='e'
)

# start: new user

component.add_transition(
    'prestart', 'start_new',
    None, {}, evaluation_transition=is_new_user
)

# start: infrequent user

component.add_transition(
    'prestart', 'start_infreq',
    None, {}, evaluation_transition=is_infreq_user
)

# start: frequent user

component.add_transition(
    'prestart', 'start_freq',
    None, {}, evaluation_transition=is_freq_user
)

component.add_transition(
    'start_new', 'receive_name',
    None, {standard_opening + " What can I call you?"}
)

component.add_transition(
    'receive_name', 'missed_name',
    None, {"i dont want to tell you"}
)

component.add_transition(
    'missed_name', 'acknowledge_name',
    None, {"Its very nice to meet you."}
)

component.add_transition(
    'receive_name', 'got_name',
    '%name=&names', {"i am an alexa prize socialbot"}
)

component.add_transition(
    'got_name', 'acknowledge_name',
    None, {"Nice to meet you, $name. $stat":0.999, "Nice to meet you":0.001}
)

component.add_transition(
    'start_freq', 'greet_freq',
    None,
    {standard_opening + " Welcome back, $name": 0.999,
     standard_opening + " Welcome back, im excited to talk to you again": 0.001},
    evaluation_transition=is_freq_user

)

component.add_transition(
    'start_infreq', 'greet_infreq',
    None,
    {standard_opening + " Its good to see you again, $name, its been a while since we last chatted": 0.999,
     standard_opening + " Its good to see you again, its been a while since we last chatted": 0.001},
    evaluation_transition=is_infreq_user
)

component.add_transition(
    'greet_infreq', 'end',
    None, {"yeah"}
)

component.add_transition(
    'greet_freq', 'end',
    None, {"yeah"}
)

component.add_transition(
    'acknowledge_name', 'end',
    None, {"yeah"}
)

component.add_transition(
    'garbage', 'end',
    None, {'thats cool'}
)

component.add_transition(
    'end', 'end', None, {'x'}, settings='e'
)

if __name__ == '__main__':
    i = input('U: ')
    while True:
        arg_dict = {"prev_conv_date": "2020-1-8 16:55:33.562881", "name": "sarah"}
        arg_dict2 = {"prev_conv_date": "2019-12-12 16:55:33.562881", "name": "sarah"}
        arg_dict3 = {"prev_conv_date": "2019-12-12 16:55:33.562881", "name": None}
        arg_dict4 = {"prev_conv_date": None, "stat": "Ive met quite a few people with your name recently."}
        if i == "hello":
            arg_dict["request_type"] = "LaunchRequest"
            arg_dict2["request_type"] = "LaunchRequest"
            arg_dict3["request_type"] = "LaunchRequest"
            arg_dict4["request_type"] = "LaunchRequest"

        using = arg_dict3
        component.vars().update({key: val for key, val in using.items() if val is not None})

        confidence = component.user_transition(i) / 10 - 0.3
        print(component.state(), component.vars())
        if component.state() == "end":
            break

        print('({}) '.format(confidence), component.system_transition())
        if component.state() == "end":
            print(component.state(), component.vars())
            break
        i = input('U: ')