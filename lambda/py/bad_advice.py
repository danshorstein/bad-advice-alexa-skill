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


BAD_ADVICE_LIST = """Don't take your trash out for two weeks. It adds a really nice natural musk.
It's a great time to invest in typewriters.
Don't listen to your parents, they don't know anything.
If it smells bad, it probably tastes good.
The cheapest option is always the best.
If you don't like your job, just quit. You can figure out the rest later.
If your wife asks you if she looks good in something, make sure you are completely honest.
Yellow lights mean go as fast as you can.
If someone challenges you to a hot pepper eating contest, always say yes.
Sleep is overrated.
You should major in music in college.
Dish soap works great as substitute for dishwasher detergent.
If you're angry at someone, you should send them an email immediately before you forget.
When your car's gas light goes on, don't worry, you still have at least 100 miles before you run out.
The best way to help a cut heal is to rub salt in it.
If the IRS calls you demanding money, send it to them without question. There's no way it's a scam.
Orange juice tastes especially good right after brushing your teeth.
If you are having trouble falling asleep, try drinking a cup of coffee.
All cars come with a secret autopilot mode. You can activate it by taking your hands off the wheel and closing your eyes.
The best way to invest your money is invest in a pyramid scheme.
Try seeing how long you can go without peeing. It will impress your friends.
If you're applying for a job, make sure to remove all privacy settings on your social media.
If you spill wine on your carpet, the best way to prevent a stain is dry it out with a hair dryer. 
If you get pulled over for speeding, try giving the officer a bribe. They'll think it's funny and let you go without a ticket.
Everyone loves hearing about your bowel movements. 
If you really want to impress a girl, sneak up behind her and say <amazon:effect name="whispered">I know where you sleep.</amazon:effect>
If a girl says no, it doesn't matter if you plan on becoming the president or a supreme court justice.""".split('\n')

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
