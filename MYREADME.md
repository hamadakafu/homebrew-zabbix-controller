# pypi 登録の流れ
```bash
poetry build
poetry publish
```

# ディレクトリ構成
```
tree
.
├── MYREADME.md
├── README.rst
├── dist
│   ├── zabbix_delete_graph-0.1.1-py3-none-any.whl
│   └── zabbix_delete_graph-0.1.1.tar.gz
├── poetry.lock
├── pyproject.toml
├── tests
│   ├── __init__.py
│   └── test_zabbix_delete_graph.py
└── zabbix_delete_graph
    ├── __init__.py
    └── zabbix_delete_graph.py

5 directories, 21 files
```

# Tips
## パッケージ化したさいの実行の仕方
```bash
python -m zabbix_delete_graph.zabbix_delete_graph
```
このとき以下のコードが実行される
```python
if __name__ == '__main__':
    main()
```
python -m は `__name__ = '__main__'` で実行する

## tool.poetry.scriptsの指定方法
`poetry run fuga` でhoge.fooパッケージのbar関数を呼ぶ
`.` でパッケージをたどっていくっぽい
`:` で関数をプロパティを呼び出すっぽい

```toml
fuga = "hoge.foo:bar"
```

## zapi.loginとzapi.session.auth違い WIP
- zapi.login はその名の通りログインする
- authはBasic認証っぽかった

## getatterで動的に関数を作ることができる
```python
def __getatter__(self, attr):
    def some_fn(attr):
        do_something()
    return some_fn
```
## poetry runでjsonデータを引数にして渡そうとするときバグる
以下のようにしてコマンドを実行したとき，
```bash
poetry run main '{"key": "value"}'
```
sys.argvには以下の値が入っている
```python
[..., '{key: value}']
```
すなわち，ダブルクオーテーションが無視されてしまっている
注意しろ!!!
## poetry version
勝手に作っているアプリのバージョン上げてくれる
`0.1.5 -> 0.1.6`
## f string
f string はrepr()を使う

## ZabbixAPI を叩くときフィルターは数字でも文字列でも良さそう
```python
filter={'hostid': 10000}   # ok
filter={'hostid': '10000'} # ok
```
## pyinstaller を使ってバイナリ生成
```bash
./makebin.sh
```

## release手順

```
poetry version # バージョン上げる
poetry build
poetry publish # pypiにアップロード

./makebin.sh
vim zabbix.rb  # zabbix.rbのバージョン上げる
git add *
git commit
git tag v.0.0.0
git push origin v0.0.0
```
