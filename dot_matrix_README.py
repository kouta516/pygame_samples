""" dot matrix display demos in pygame (and minecraft)

dot_matrixモジュール：
m列 x n行のマトリクスをpygame用/minecraft用に描くクラス定義とPygame用のサンプルコードを持つ。
dot_matrix.py
    クラス定義
        Matrix, MatrixPG, MatrixMC, Scanner
    サンプルコード部分
        pygame出力/自動移動のみ、キー操作なし
        インスタンスは2つ（フレームありとなし、リスト／イテレーションなし）
class Matrix:  # parent class
    def __init__(self, m, n, colors, with_frame):
class MatrixPG(Matrix):  # child class for pygame
    def __init__(self, screen, m=5, n=7, dot_size=15, dot_intv=18, colors=None, wait=0.1, x0=1, y0=1):
class MatrixMC(Matrix):  # child class for minecraft
    def __init__(self, mc, m=5, n=7, colors=None, wait=0.1, x0=1, y0=1, z0=1)
class Scanner:
    def __init__(self, matrix, pos=None, change=None, wait=0.2, direction="horizontal"):


デモコード：  （注意）dotmartrixモジュールを使っている。
demo_dot_matrix_all.py
    全部入り: pygame/minecraft x 自動移動／キー操作 x 複数インスタンス
    インスタンスのリスト／イテレーションループ化、キーチェック関数、インスタンスのアップデート関数
    操作キーとパラメーターの辞書化
    複数インスタンスの扱い方の参考になる。

サンプルコード：  （注意）dotmartrixモジュールを使っている。 （未完）
demo_dot_matrix_sample0.py  pygameだけを使う、最もシンプルな例
demo_dot_matrix_sample2.py  minecraftだけを使う、最もシンプルな例
demo_dot_matrix_sample3.py  pygameとminecraftを使う、最もシンプルな例

演習用コード：  （注意）dot_matrixモジュールを使わず、クラス定義がないもの、ファイル内に定義してあるものがある。最終形のdot_matrixモジュールとの互換性がない部分もあるので注意すること。
demo_dot_matrix_pg0.py「最初の一歩」
    pygame、自動移動、クラスを使わず直接書いたもの
demo_dot_matrix_pg1.py「クラス化演習」
    pygame、自動移動、クラス（継承なし）、課題：複数インスタンス（リスト/ループなし）
demo_dot_matrix_pg2.py「イテレーションループ演習」
    pygame、自動移動、複数インスタンス（リスト/ループあり）
demo_dot_matrix_scan0.py「スキャナークラス追加演習」
    Scannerクラス（自動移動のみ、水平／垂直移動）
demo_dot_matrix_key0.py「キー入力対応演習」
    pygame、自動移動、キー入力、課題：Scannerにキー操作メソッドを追加
demo_dot_matrix_mc0.py「マイクラ対応演習」
    pygame、マイクラ、自動移動、クラスなし
demo_dot_matrix_mc1.py「クラス継承化演習」
    pygame、マイクラ、自動移動、クラス継承


1. クラス化演習（同ファイル内）
    demo_dot_matrix_pg0.py　→　demo_dot_matrix_pg1.py
    差分：Matrixクラス追加（自動移動のみ）
    メモ：自動スキャンはメインループに直接書く。インスタンスは２つ。
    課題：Matrixインスタンスを追加する。
2. スキャナークラス追加演習（同一ファイル内）
    demo_dot_matrix_pg0.py　→　demo_dot_matrix_scan0.py
    差分：Scannerクラス（自動移動のみ）追加。
    メモ：自動スキャンをScannerクラスに移動。
    課題：Scannerクラスにキー操作メソッドを追加。
3. キー入力対応演習
    demo_dot_matrix_pg0.py　→　demo_dot_matrix_key0.py
    差分：キー入力対応追加
    メモ：クラスなし、極力シンプル状態。キー入力はメインループに直接書く。
4. イテレーション演習
    demo_dot_matrix_scan0.py　→　demo_dot_matrix_pg2.py
    差分：リストとイテレーションループ
    メモ：Matrixの複数インスタンスのリスト化／イテレーションループ化。
    課題：Scannerのリスト化／イテレーションループ化。
5. クラス継承化演習（同一ファイル内）
    demo_dot_matrix_pg1.py　→　demo_dot_matrix_mc1.py
    差分：MatrixPGクラス、MatrixMCクラス追加（自動移動のみ）
    メモ：Matrixクラスを継承して、MatrixPGクラス、MatrixMCクラスを追加。自動移動はメインループのまま。
6. マイクラ対応演習
    demo_dot_matrix_pg0.py　→　demo_dot_matrix_mc0.py
    差分：マイクラ対応（クラスなし）
7. クラスをモジュールに分離する演習（未完）
    demo_dot_matrix_pg0.py　→　demo_dot_matrix_pg3.py、dot_matrix_pre.py
    差分：クラス定義部分をモジュールdot_matrix_preに分離
    メモ：pygameのみ、自動移動のみ、複数インスタンス（リスト/ループなし）、キー操作なし、Scannerクラスなし

番外編（未完）
ドットマトリクスフォント表示との統合
    DotMatrixFontDisplayクラス（改造版）
        Matrixクラスを継承
        さらに、DotMatrixFontDisplayPG, DotMatrixFontDisplayMCへ。
        Matrixを水平方向、垂直方向に拡張、フレームを付ける。カラム、ロウを指定して文字を表示できるようにする。
        on/off/frame/background色を指定できる。(Matrixのcolorsを継承)
        frameの幅を指定できるようにする。（Matrixのframeを継承）
    print_text、print_numメソッドを追加
"""
