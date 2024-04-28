from caveinfo_converter import CaveInfoConverter
import traceback
from browser import document, window, alert
yaml = window.jsyaml

def convert_test(event):
    input_text: str = document['input-area'].value
    reader = CaveInfoConverter()
    try:
        output_dict = reader.to_dict(input_text)
        document['output-area'].value = yaml.dump(output_dict)
    except Exception as e:
        alert('Could not convert:\n' + traceback.format_exc())
document['convert-button'].bind('click', convert_test)