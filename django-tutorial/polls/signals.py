from django.core.signals import request_started
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver, Signal
# Be sure to 'import polls.apps.signals' in the
# PollsConfig.ready() method of polls.app.py

from .logger import POLLS_BOTH_SIGNALS as logger

LOGGING_ACTIVATED = False

pdf_done = Signal(providing_args=['user', 'filename', 'engine'])


@receiver([request_started])
def log_request(sender, **kwargs):
    global LOGGING_ACTIVATED

    if LOGGING_ACTIVATED:
        logger.debug(f"--> log_request in /tmp/polls_signal.log")

        env = kwargs['environ']
        host = env['HTTP_HOST']
        server = env['SERVER_NAME']
        method = env['REQUEST_METHOD']
        path = env['PATH_INFO']
        query = env['QUERY_STRING']

        logger.info(f"{method} REQUEST STARTED on {host} {server}. {path}?{query}")


@receiver([user_logged_in])
def log_user(sender, **kwargs):
    logger.debug(f"--> {sender}")
    logger.debug(f"--> {kwargs}")
    logger.debug(f"--> log_user in /tmp/polls_signals.logl")

    global LOGGING_ACTIVATED
    LOGGING_ACTIVATED = True

    user = kwargs['user']
    request = kwargs['request']
    logger.info(f"LOGGING ACTIVATED: {user} {request}")


@receiver(pdf_done)
def log_pdf(sender, **kwargs):

    user = kwargs['user']
    engine = kwargs['engine']
    filename = kwargs['filename']

    logger.info(f"{user} generated {filename} using {engine}")

