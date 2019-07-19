# TODO: デフォルトで1つしか更新しないようにして，--allow-manyで複数更新できるようにしたい
# TODO: 確認をしないyesオプション
# TODO: 複数の条件をマッチできるようにする and はできた．or がまだ
# TODO: --dry-runをつかってテストできるようにする

# TODO: 本当は，gcpのインスタンスがあるかどうかのチェックをする
# TODO: zabbixにあるhostidとかhostnameと比較して，集合の差をとる (zabbix.hostname - gcp.instancename)

from . import command
from . import utils
from . import hosts
from . import zabbix_ctl
