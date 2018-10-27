# -*- coding: utf-8 -*-

# This is a simple Bad Advice giving Alexa Skill, built using
# the decorators approach in skill builder.
import logging
import random
from io import StringIO
import time

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


BAD_ADVICE_LIST = """You should sleep on that French braid!
Just hide it in your backpack — they can’t search your person.
You should just drive to Toronto; it’s so much easier than flying.
You have to join this club called Columbia House. They mail you any 12 CDs for only 99¢!
How can you tell if you’re really allergic to it unless you eat some more?
Try this! It’s blue.
Take the train — it’s such a romantic way to travel.
Just go to the dental school, it’s much cheaper and they’ve learned most of the important stuff already.
You should dye your hair blond.
You should dye your hair black.
You should grow your hair really long, like past your boobs.
You should shave your head.
You should get a body wave!
You should always wear hats.
No, it’s definitely the left side for appendicitis.
You’re fine! Just chug a glass of water and let’s go to the next bar.
A college essay is supposed to be funny.
You should take the overnight bus — its 11 hours but you’ll sleep practically the whole time.
It’s actually easier to learn to drive on a standard.
You should just sing that oral report.
You don’t actually have to serve jury duty unless it’s for the county in which you were born.
Feed a fever, drown a cold.
The best cure for poison ivy? Bleach.
Just glue it back together. Your parents will never notice.
No, I’m pretty sure you can’t study for AP exams.
You don’t really need any equipment for camping.
It’s fine. Dogs can only give rabies to other dogs, not humans.
Just get really drunk before you get on the plane.
A vibrant yellow is perfect for your bedroom because it’s so cheerful.
You can make it — gun it.
You can’t get scarlet fever twice.
You should climb in her window and leave a note on her pillow. It’s so romantic.
Don’t bother bringing a map — we can just ask someone.
It’s not a big deal, jump in. No one ever remembers this, but people just instinctually know how to swim.
Times Square is the only place to be on New Year’s Eve.
You should go to the Village Halloween parade! It’s awesome.
You’ve never been to the St. Patrick’s Day parade? We’re going.
The Zodiac killer is just an urban legend.
Oh no, bread can’t expire.
Permanent markers aren’t actually permanent.
Shake it off. It doesn’t look broken and a sprain actually hurts worse than a break.
Just major in whatever you’re most interested in.
Always, always, keep batteries in the freezer.
You can’t get scarlet fever three times.
Don’t rehearse, it’s more spontaneous.
You can’t get motion sickness on the Gravitron because it’s going in a circle.
It he tries to mug you just play dead. Or run away in a zigzag pattern.
Why don’t you write both papers at once? It’ll be faster.
Babysitting is a great way to make some extra money, plus kids are so cute.
Just rub a cold washcloth on your sore throat—it’s soothing.
Scoliosis is an old wives’ tale.
“Liquor before beer unless it’s clear.” So, like, just get something gin-based.
Don’t smell it; just eat it really fast.
That’s only in the movies. No one ever actually gets caught pulling the fire alarm.
I think you should go with the Fung Wah bus; it’s only $15 a ticket.
For the last time, you can keep holding it. Sparklers go out on their own.
There is no “too early” when it comes to “I love you.”
Baking soda and baking powder are the same thing; this cake is going to be delicious.
Owls are great pets!
Buy it on Canal Street. They never raid those Chinatown stands anymore.
Don’t take anymore than two shots before the presentation, but definitely take at least one.
Tupperware can go in the oven as long as it’s below 375?
Go running later, when it’s dark — that way the park will be less crowded.
A great first date is going to a comedy club, or get one of those tandem bicycles. Or both!
You don’t need an electrician for that — just do it yourself.
Grapes have no nutritional value.""".split('\n')

def select_random_bad_advice(bad_advice_list):
    return random.choice(bad_advice_list)


def get_random_yes_no_question():
    return random.choice([
        'Do you want another terrible piece of advice?',
        'Would you like more terrible suggestions?',
        'Might you want another little nugget of non-wisdom?'
    ])


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to terrible advice. You can say 'give me some advice' to ask for terrible advice."

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Terrible Advice", speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("BadAdviceIntent"))
def bad_idea_intent_handler(handler_input):
    """Handler for Bad Advice Intent."""
    # type: (HandlerInput) -> Response
    speech_text = (f'Here is your terrible advice: {select_random_bad_advice(BAD_ADVICE_LIST)} ' +
            (f'{get_random_yes_no_question()}'))

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Terrible Advice", speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.YesIntent"))
def yes_intent_handler(handler_input):
    """If user says Yes, they want another piece of Terrible advice"""
    # type: (HandlerInput) -> Response
    logger.info('In YesHandler')
    return bad_idea_intent_handler(handler_input)


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.NoIntent"))
def no_intent_handler(handler_input):
    """If user says No, they are done"""
    # type: (HandlerInput) -> Response
    logger.info('In NoHandler')
    speech_text = 'Ok, bye bye now!'
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Terrible Advice", speech_text)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can say 'give me some terrible advice!'"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Terrible Advice", speech_text)).response


@sb.request_handler(can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Hope you don't take my advice! Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Terrible Advice", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Terrible Advice skill can't help you with that.  "
        "You can say give me some advice!!")
    reprompt = "You can say give me some advice!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, I was not paying attention and didn't hear anything you just said. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()
