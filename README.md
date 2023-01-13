# はじめに

このパッケージはMISLで開発しているDEAPの追加ライブラリです。  
DEAPのモジュールと同じ構成になっています。

# パッケージ構造

## deap_misl.tools

各種GA操作（オペレータ）です。  
deap.toolsと同じようにtoolboxに登録して利用します。

なお、deap.toolsも使う場合は

```py
from deap_misl import tools as misl_tools
```

のように別名をつけるようにしてください。

## deap_misl.algorithms

GA操作ではなく、アルゴリズム全体を実行する関数です。
