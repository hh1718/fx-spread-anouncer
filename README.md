# usage

## 前提
pythonv3以降をインストールしていること。(macであればデフォルトでインストールされてます)

## セットアップ(初回だけ)
requirements.txtを使って以下のようにもできる
```
cd src
rm -rf packages //packagesディレクトリを削除
mkdir packages  //packagesディレクトリを作成
pip install -r ../requirements.txt -t packages
cd ../
```
以下のように個別にインストールしても問題なし
```
cd src
rm -rf packages //packagesディレクトリを削除
mkdir packages //packagesディレクトリを作成
pip install requests -t packages
pip install pyttsx3 -t packages
pip install beautifulsoup4 -t packages
pip install selenium -t packages
pip install webdriver-manager -t packages
cd ../
```
※macの場合はpip3 installのはずです。windowsの場合 pip installのオプションに`--no-user`が必要かもしれないです。


## start
```
python src/main.py
```
※macの場合はpython3 src/main.pyのはずです。初回は必ず読み上げられます。

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