class WUWInterface:
    def prepare(self) -> None:
        pass

    def process(self) -> bool:
        pass

    def terminate(self) -> None:
        pass


class WUWFeedbackInterface:
    def start_listening_feedback(self):
        pass

    def end_listening_feedback(self):
        pass

    def terminate(self):
        pass
