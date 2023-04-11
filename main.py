"""
DocumentCloud Add-On that translates documents using Google Translate services.
"""
import six
from google.cloud import translate_v2 as translate
from util.constants import ENCODING_STANDARD
from documentcloud.addon import AddOn


class Translate(AddOn):
    """DocumentCloud premium Add-On that translates documents"""

    def main(self):
        input_lang = self.data.get("input_lang")
        output_lang = self.data.get("output_lang" 
        if len(input_lang) != 2:
            self.set_message(
                "You submitted an improper ISO language code as an input. "
                "It is supposed to be two characters in length."
            )
            sys.exit(1)
        if len(output_lang) != 2:
            self.set_message(
                "You submitted an improper ISO language code. "
                "It is supposed to be two characters in length."
            )
            sys.exit(1)                         
                                    
                                    
        for document in self.get_documents():
            


if __name__ == "__main__":
    Translate().main()
