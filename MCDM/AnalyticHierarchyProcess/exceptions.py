
class AHPException(Exception):
    def __init__(self, text="AHP Exception"):
        self.text = text
        super().__init__(self.text)
