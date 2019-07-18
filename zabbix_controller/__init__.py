# TODO: デフォルトで1つしか更新しないようにして，--allow-manyで複数更新できるようにしたい
# TODO: ZabbixCTL をいい感じにプリントするようにする．引数とかを保存してもいいかもしれない．
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
