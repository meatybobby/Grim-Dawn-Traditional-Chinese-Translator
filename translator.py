import argparse
import os
import requests
import tempfile
import subprocess

parser = argparse.ArgumentParser(description='Translate Simplified Chinese to Traditional Chinese')
parser.add_argument('--input_arc', type=str)
parser.add_argument('--base_arc', type=str, default=None)
parser.add_argument('--output_arc', type=str, default="Text_ZH.arc")
parser.add_argument('--grim_path', type=str)

grim_path = "C:\\SteamLibrary\\steamapps\\common\\Grim Dawn"
input_arc = "C:\\SteamLibrary\\steamapps\\common\\Grim Dawn\\resources\\Text_ZH.arc"

def translate(input_text):
    url = 'https://api.zhconvert.org/convert'
    data = {
        "text": input_text,
        "apiKey": "",
        "ignoreTextStyles": "",
        "jpTextStyles": "",
        "jpTextConversionStrategy": "protectOnlySameOrigin",
        "jpStyleConversionStrategy": "protectOnlySameOrigin",
        "modules": "{\"ChineseVariant\":\"0\",\"Computer\":\"0\",\"EllipsisMark\":\"0\",\"EngNumFWToHW\":\"0\",\"GanToZuo\":\"-1\",\"Gundam\":\"0\",\"HunterXHunter\":\"0\",\"InternetSlang\":\"-1\",\"Mythbusters\":\"0\",\"Naruto\":\"0\",\"OnePiece\":\"0\",\"Pocketmon\":\"0\",\"ProperNoun\":\"-1\",\"QuotationMark\":\"0\",\"RemoveSpaces\":\"0\",\"Repeat\":\"-1\",\"RepeatAutoFix\":\"-1\",\"Smooth\":\"-1\",\"TengTong\":\"0\",\"TransliterationToTranslation\":\"0\",\"Typo\":\"-1\",\"Unit\":\"-1\",\"VioletEvergarden\":\"0\"}",
        "userPostReplace": "",
        "userPreReplace": "",
        "userProtectReplace": "",
        "diffCharLevel": 0,
        "diffContextLines": 1,
        "diffEnable": 1,
        "diffIgnoreCase": 0,
        "diffIgnoreWhiteSpaces": 0,
        "diffTemplate": "Inline",
        "cleanUpText": 0,
        "ensureNewlineAtEof": 0,
        "translateTabsToSpaces": -1,
        "trimTrailingWhiteSpaces": 0,
        "unifyLeadingHyphen": 0,
        "converter": "Taiwan"
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    res = r.json()
    return res["data"]["text"]

def iterate_trans_dir(unpack_input, unpack_base, output_path):
    input_dir = os.listdir(unpack_input)[0]
    base_dir = os.listdir(unpack_base)[0]
    for root, subFolder, files in os.walk(unpack_input):
        for f in files:
            path = os.path.join(root, f)
            base_path = path[len(unpack_input):]
            output_file = output_path + base_path
            output_dir = os.path.dirname(output_file)

            os.makedirs(output_dir, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as fw:
                new_dict = {}
                if unpack_base:
                    base_file = path.replace(f"text_org\\{input_dir}", f"text_base\\{base_dir}")
                    with open(base_file, "r", encoding="utf-8") as fd:
                        for s in fd:
                            fw.write(s)
                            if "=" in s:
                                key = s.split("=")[0]
                                new_dict[key] = ""

                with open(path, "r", encoding="utf-8") as fd:
                    append_str = []
                    for s in fd:
                        if "=" in s:
                            key = s.split("=")[0]
                            if not key in new_dict:
                                append_str.append(s)

                if append_str:
                    final_str = "".join(append_str)
                    final_str = translate(final_str)
                    fw.write("\n#Auto Translate\n")
                    fw.write(final_str)

def unpack_arc(arc_exe, input_arc, output_path):
    subprocess.run([arc_exe, input_arc, "-extract", output_path], check=True)

def pack_arc(arc_exe, input_path, output_arc):
    subprocess.run([arc_exe, output_arc, "-update", ".", input_path, "6"], check=True)

if __name__ == "__main__":
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tempdir:
        unpack_input = os.path.join(tempdir, "text_org")
        grim_path = args.grim_path if args.grim_path is not None else grim_path
        input_arc = args.input_arc if args.input_arc else input_arc

        arc_exe = os.path.join(grim_path, "ArchiveTool.exe")
        unpack_arc(arc_exe, input_arc, unpack_input)

        unpack_base = None

        if args.base_arc:
            unpack_base = os.path.join(tempdir, "text_base")
            unpack_arc(arc_exe, args.base_arc, unpack_base)

        unpack_temp = os.path.join(tempdir, "temp")
        iterate_trans_dir(unpack_input, unpack_base, unpack_temp)

        input_dir = os.listdir(unpack_temp)[0]
        unpack_path = os.path.join(unpack_temp, input_dir)
        pack_arc(arc_exe, unpack_path, args.output_arc)