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

### tools.selNSGA2

DEAPに含まれているselNSGA2を設計変数シェアリング（設計変数空間での混雑度による間引き）も行えるようにしたものです。

サンプルファイル：examples/multi_knapsack_nsga2.py

### tools.selNSGA3

DEAP本体にもNSGA3が含まれるようになりましたが、それより前にMISLで実装していたNSGA3です。

サンプルファイル：examples/nsga3.py

## deap_misl.algorithms

GA操作ではなく、アルゴリズム全体を実行する関数です。

### algorithms.moead

MOEA/Dの実装です。

サンプルファイル：examples/moead_onemax.py

