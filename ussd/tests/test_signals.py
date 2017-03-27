from structlog import get_logger

from ussd.signals import session_started, session_ended
from ussd.tests import UssdTestCase

test_session_id_arrived = []


def session_started_notification(**kwargs):
    logger = get_logger(__name__).bind(
        action="Session Started signal",
        **kwargs
    )
    logger.info("Signal arrived")
    test_session_id_arrived.append(kwargs.get('session_key'))


def session_ended_notification(**kwargs):
    logger = get_logger(__name__).bind(
        action="Session End signal",
        **kwargs
    )
    logger.info("Signal arrived")
    test_session_id_arrived.append(kwargs.get('session_key'))


session_started.connect(session_started_notification)
session_ended.connect(session_ended_notification)


class TestSignals(UssdTestCase.BaseUssdTestCase):
    validate_ussd = False

    def get_ussd_client(self):
        return self.ussd_client(
            generate_customer_journey=False,
            extra_payload={
                "customer_journey_conf": "valid_signals_conf.yml"
            }
        )

    def test_signal_is_sent_and_received_by_subscribers(self):
        ussd_client = self.get_ussd_client()

        # dial in
        response = ussd_client.send('')
        print(response)
        print(len(test_session_id_arrived))
        self.assertTrue(len(test_session_id_arrived) > 1)
