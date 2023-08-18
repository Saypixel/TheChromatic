class MutualText:
    text = ""
    prefix = ""
    delay = 1

    index = 0

    def __init__(self, text: str, prefix: str, delay: int):
        self.text = text
        self.prefix = prefix
        self.delay = delay
