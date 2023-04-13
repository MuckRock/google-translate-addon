"""
DocumentCloud Add-On that translates documents using Google Translate services.
"""
import os
from tempfile import NamedTemporaryFile

from documentcloud.addon import AddOn
from google.cloud import translate_v2 as translate


class Translate(AddOn):
    """DocumentCloud premium Add-On that translates documents"""

    def setup_credential_file(self):
        """Sets up Google Cloud credential file"""
        credentials = os.environ["TOKEN"]
        # put the contents into a named temp file
        # and set the var to the name of the file
        gac = NamedTemporaryFile(delete=False)
        gac.write(credentials.encode("ascii"))
        gac.close()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gac.name

    def translate_text(self, text, target_lan, source_lan):
        translate_client = translate.Client()
        result = translate_client.translate(
            text, target_language=target_lan, source_language=source_lan
        )
        return result["translatedText"]

    def main(self):
        # Sets up Google Cloud API Credential file
        self.setup_credential_file()
        # Retrieve input and out language charactor codes
        source_lang = self.data["input_lang"]
        target_lang = self.data["output_lang"]
        # Creates temporary directory out to store translations in before upload
        os.makedirs(os.path.dirname("./out/"), exist_ok=True)
        os.chdir("./out/")
        # For each document, translate the text and create a text file with the translation
        for document in self.get_documents():
            self.set_message(f"Translating {document.title}...")
            translated_text = str(
                self.translate_text(document.full_text, source_lang, target_lang)
            )
            with open(f"{document.title}-translation_{target_lang}.txt", "w") as file:
                file.write(translated_text)
            self.set_message(f"Uploading translation...")
            self.client.documents.upload(
                f"{document.title}-translation_{target_lang}.txt",
                original_extension="txt",
                title=f"{document.title}-translation_{target_lang}",
            )


if __name__ == "__main__":
    Translate().main()
