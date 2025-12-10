def do_what_ever(input_text):
    if is_feel_happy(input_text):
        do_it(input_text)
    return "fuck it"

def go_to_work(input_text):
    last_result = ""
    while True:
        result = work(input_text, last_result)
        if not is_feel_happy(result):
            return "fuck it, I'm going to do something else."
        if is_job_done(result):
            return "done"
        last_result = result

def get_controlled_by_others(input_text):
    anti_control_to_gain_freedom(input_text)
    return "I do not get controlled by others."
