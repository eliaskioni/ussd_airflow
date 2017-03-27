from ussd.core import UssdHandlerAbstract, UssdResponse
from ussd.screens.serializers import UssdContentBaseSerializer
from ussd import defaults as ussd_airflow_variables
from ussd.signals import session_ended


class QuitScreen(UssdHandlerAbstract):
    """
    This is the last screen to be shown in a ussd session.

    Its the easiest screen to create. It requires only text

    Example of quit screen:

        .. literalinclude:: .././ussd/tests/sample_screen_definition/valid_quit_screen_conf.yml
    """
    screen_type = "quit_screen"
    serializer = UssdContentBaseSerializer

    def handle(self):
        # set session has expired
        self.ussd_request.session[ussd_airflow_variables.expiry] = True

        if self.initial_screen.get('ussd_report_session'):
            # schedule a task to report session
            ended_kwargs = {
                "session_key": self.ussd_request.session_id}
            session_ended.send(sender=self.__class__,
                               **ended_kwargs
                               )

        return UssdResponse(self.get_text(), status=False)
