# はじめに

このリポジトリはMISLで開発しているDEAPのライブラリです。
DEAPのモジュールと同じ構成にしてあります。

# deap_misl.tools

各種GA操作です。
deap.toolsと同じようにtoolboxへの登録を行います。

なお、deap.toolsも使う場合は
from deap_misl import tools as misl_tools
のように別名をつけるようにしてください。

## tools.selNSGA2

DEAPに含まれているselNSGA2を設計変数シェアリング（設計変数空間での混雑度による間引き）も行えるようにしたものです。

サンプルファイル：examples/multi_knapsack.py

## tools.selNSGA3

大沢さんによるNSGA3の実装です。

サンプルファイル：examples/nsga3.py

## tools.cxTwoPoint2d

二次元交叉の実装です。

サンプルファイル：examples/onemax_2d.py
※二次元遺伝子では突然変異も工夫が必要です。サンプルファイルをご参照ください。

# deap_misl.algorithms

GA操作ではなく、アルゴリズム全体を実行する関数です。

## algorithms.moead

MOEA/Dの実装です。

サンプルファイル：examples/moead_onemax.py

