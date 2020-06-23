from googletrans import Translator
import pandas as pd
from HindiTokenizer import Tokenizer


if __name__ == "__main__":
    data = pd.read_csv('/Windows/Data/dainik_07012020.csv')
    for ind in data.index:
        print([data.loc[ind]['Article']])
        translator = Translator()
        translations = translator.translate(str([data.loc[ind]['Article']]), dest='en')
        for translation in translations:
            print(translation.text)
