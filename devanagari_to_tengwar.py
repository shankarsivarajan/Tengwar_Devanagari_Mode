import json
from pathlib import Path
import argparse 
import numpy as np
import re

replace_numbers_devanagari_latin = '''
{"\u0966": "0", "\u0967": "1", "\u0968": "2", "\u0969": "3", "\u096a": "4", "\u096b": "5", "\u096c": "6", "\u096d": "7", "\u096e": "8", "\u096f": "9"}
'''

replace_numbers_latin_tengwar = '''
{"0": "\ue070", "1": "\ue071", "2": "\ue072", "3": "\ue073", "4": "\ue074", "5": "\ue075", "6": "\ue076", "7": "\ue077", "8": "\ue078", "9": "\ue079", "A": "\ue07a", "B": "\ue07b"}
'''

replace_devanagari = '''
{"\u0905": "\ue02e", "\u0906": "\ue02c", "\u0907": "\ue02e\ue044", "\u0908": "\ue02c\ue044", "\u0909": "\ue02e\ue04c", "\u090a": "\ue02c\ue04c", "\u090b": "\ue020", "\u0960": "\ue020\ue02c", "\u090c": "\ue021", "\u0961": "\ue021\ue02c", "\u090f": "\ue02c\ue046", "\u0910": "\ue02a", "\u0913": "\ue02c\ue04a", "\u0914": "\ue02b", "\u0915": "\ue003", "\u0916": "\ue003\ue051", "\u0917": "\ue007", "\u0918": "\ue007\ue051", "\u0919": "\ue013", "\u091a": "\ue002", "\u091b": "\ue002\ue051", "\u091c": "\ue006", "\u091d": "\ue006\ue051", "\u091e": "\ue013\ue043", "\u091f": "\ue000", "\u0920": "\ue000\ue051", "\u0921": "\ue004", "\u0922": "\ue004\ue051", "\u0923": "\ue012", "\u0924": "\ue008", "\u0925": "\ue008\ue051", "\u0926": "\ue00c", "\u0927": "\ue00c\ue051", "\u0928": "\ue010", "\u092a": "\ue001", "\u092b": "\ue001\ue051", "\u092c": "\ue005", "\u092d": "\ue005\ue051", "\u092e": "\ue011", "\u092f": "\ue016", "\u0930": "\ue014", "\u0932": "\ue022", "\u0935": "\ue017", "\u0936": "\ue027", "\u0937": "\ue027\ue051", "\u0938": "\ue025", "\u0939": "\ue028", "\u0933": "\ue023", "\u093e": "\ue02c", "\u093f": "\ue044", "\u0940": "\ue02c\ue044", "\u0941": "\ue04c", "\u0942": "\ue02c\ue04c", "\u0943": "\ue020", "\u0944": "\ue020\ue02c", "\u0962": "\ue021", "\u0963": "\ue021\ue02c", "\u0947": "\ue02c\ue046", "\u0948": "\ue02a", "\u094b": "\ue02c\ue04a", "\u094c": "\ue02b", "\u0902": "\ue050", "\u0903": "\ue040", "\u094d": "\ue045", "\u0964": "\ue065", "\u0965": "\ue065\ue065", "\u0966": "\ue070", "\u0967": "\ue071", "\u0968": "\ue072", "\u0969": "\ue073", "\u096a": "\ue074", "\u096b": "\ue075", "\u096c": "\ue076", "\u096d": "\ue077", "\u096e": "\ue078", "\u096f": "\ue079", "\u093d": "\ue02d"}
'''

lsd_marker = "\ue07d"

replace_dict_numbers_devanagari = json.loads(replace_numbers_devanagari_latin)
replace_dict_numbers_latin = json.loads(replace_numbers_latin_tengwar)
replace_dict_devanagari = json.loads(replace_devanagari)

def transliterate_integers(input_string):
    
    # Tengwar integers are written right-to-left, in base 12, with a marker after the least significant digit.
    
    # The fractional part will be treated as a separate integer. :(
    
    for key, value in replace_dict_numbers_devanagari.items():
        input_string = input_string.replace(key, value)
            
    all_nums = re.findall(r'\d+', input_string)
    all_nums.sort(key=lambda s: -len(s)) # replace the longest strings first to stop substrings getting replaced.
    
    for regular_number in all_nums:
        tengwar_number = np.base_repr(int(regular_number), base=12)
        
        for key, value in replace_dict_numbers_latin.items():
            tengwar_number = tengwar_number.replace(key, value)
        
        tengwar_number = tengwar_number[::-1][0] + lsd_marker + tengwar_number[::-1][1:]
        
        input_string = input_string.replace(regular_number, tengwar_number)
        
    return input_string


def transliterate(input_file, output_file):
    
    if output_file == "":
        output_file = Path(input_file).stem + '_tengwar.txt'
    
    with open(input_file, 'r', encoding="utf-8") as file:
        devanagari_text = file.read()
        
        devanagari_text = transliterate_integers(devanagari_text)
        
        for key, value in replace_dict_devanagari.items():
            devanagari_text = devanagari_text.replace(key, value)
    
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(devanagari_text)
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Transliterate Devanagari to Tengwar.")
    parser.add_argument("input", help="Input file, in Devanagari.")
    parser.add_argument("output", nargs = '?', help="Output file, in Tengwar.", default = "")

    args = parser.parse_args()
    transliterate(args.input, args.output)
    
    print("Done!")