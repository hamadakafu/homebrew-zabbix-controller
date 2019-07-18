# TODO: ディレクトリ構成をきれいな階層構造にする
# TODO: デバッグモードを追加する．デバッグモードではapiを叩かない
# TODO: フィルターの際に時間で指定できるようにする．hostしか時間はわからなそう
# TODO: デフォルトで1つしかターゲットにしないようにする．manyオプションで複数操作できるようにする
# TODO: 確認する際にbulletではなくclickのconfirmationメソッドで行う
# TODO: インタラクティブじゃないquietオプション
# TODO: 確認をしないyesオプション
# TODO: 複数の条件をマッチできるようにする

# TODO: 本当は，gcpのインスタンスがあるかどうかのチェックをする
# TODO: zabbixにあるhostidとかhostnameと比較して，集合の差をとる (zabbix.hostname - gcp.instancename)

from . import command
from . import utils
from . import hosts
from . import zabbix_ctl
