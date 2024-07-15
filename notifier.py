import logging


class Notifier:
    def notify(self, message: str):
        raise NotImplementedError("Subclass please implement this")


class ConsoleNotifier(Notifier):
    def notify(self, message: str):
        logging.info(message)
