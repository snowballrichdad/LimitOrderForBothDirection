# LimitOrderForBothDirection
auカブコム証券のkabuステーションAPIを使用したW指値プログラムです

信用取引で
1. 成行で新規
2. 価格を監視し
3. 利食いで指定した価格になるとIOC指値で返済
4. 損切りでした価格になると成行で返済

することによってW指値を実現しています。

詳しくはブログで解説しています。
http://snowballrichdad.xyz/post-6345/
