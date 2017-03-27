from django.dispatch import Signal

session_started = Signal(providing_args=["session_key"])
session_ended = Signal(providing_args=["session_key"])