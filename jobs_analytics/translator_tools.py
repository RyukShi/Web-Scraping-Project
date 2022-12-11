from googletrans import Translator


class TranslatorTools():

    def __init__(
        self,
        default_dest: str = "fr"
    ):
        self.translator = Translator()
        self.default_dest = default_dest

    def translate(self, text):
        try:
            return self.translator.translate(text, dest=self.default_dest)
        except ValueError as e:
            print(f"Translation process failed, Error: {e}")


def main():
    translator_tools = TranslatorTools()
    l = ["東京都, 日本", "창원 지역", "福岡"]
    for txt in l:
        translate_txt = translator_tools.translate(txt)
        print(translate_txt)


if __name__ == '__main__':
    main()
