# usage

## 前提
pythonv3以降をインストールしていること。(macであればデフォルトでインストールされてます)

## セットアップ(初回だけ)
setup.batをダブルクリック、もしくはコマンドプロンプトで以下を実行
```
backup.bat
```


## start
start.batをダブルクリック、もしくはコマンドプロンプトで以下を実行
```
python src/main.py
```

※ 実行時に
```
  import pywintypes
ImportError: No module named pywintypes
```
というエラーが出た場合は fx-price-anouncer/src/packages/pywin32_system32内のpythoncom310.ddlとpywintypes310.ddlというファイルをfx-price-anouncer/src/packages/win32/lib/にコピーしてください


## 設定ファイル
config.jsonが設定ファイルです。
```
{
    "announce_order": ["gaikaex", "gaitame", "rakuten"], // 読み上げる会社の順番
    "time_interval": 2, //データ更新頻度(秒)
    "force_anounce_per": 5, //データの更新の有無にかかわらず強制的に読み上げるデータ取得頻度. 0以下の場合はデータに変更がある場合のみ読み上げ
    "target_pair": "usdjpy", // 対象の通過ペア, "usdjpy" or "eurjpy" or "gbpjpy" or "audjpy" or "nzdjpy"
    "logging": true. //logを出力するか true or false
}
```

## 全通貨読み上げ(テスト用)
```
python src/all-pair/gaitame.py
python src/all-pair/gaikaex.py
python src/all-pair/rakuten.py
```