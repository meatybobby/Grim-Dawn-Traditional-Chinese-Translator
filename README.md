# Grim-Dawn-Traditional-Chinese-Translator
翻譯Grim Dawn的簡體語言包(.arc)成繁體中文

By https://zhconvert.org "台灣化" converter.

## 使用方法
```bash
python translator.py --grim_path <path of Grim Dawn root> --input_arc <path of Simplified Chinese .arc> --output_arc <output path> [--base_arc <path of base arc>]
```

`--base_arc` 非必要，如果有提供，將使用base arc做基底，只翻譯未包含在base arc的內容

推薦的基底: https://ksinwei.me/gaming/grim-dawn/traditional-chinese/
