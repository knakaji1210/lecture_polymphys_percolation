# lecture_polymphys_percolation

講義「高分子物理学特論」の#5「Polymer Gels」で利用

＜未解決問題＞
n_s(p_c)のs依存性（フィッシャー指数）がおかしい。これはn_s(p)全体に関係する可能性があり、見直すとすれば全体を見直す必要がある。
その際、np.ndarrayで組み直すべきか。
Forestfireでsごとに（色分けして）結果を描画
ヒストグラムの横軸がずれている問題

上記n_s(p_c)に対するコメント（250202）
n_s(p_c)について、これはPクラスターができたところなので、それ以外のクラスターの個数はp < p_cの時に比べて小さくなる。でもn_s(p)/n_s(p_c)はexp(-s)とならねばならないので、n_s(p=p_c)ではなく、n_s(p~p_c)と比較すべきなのではないかと思い至った。そのプログラム上の修正は行なっているが、今後精査していくべき

curveFit_critical_S_v4.pyについて
Sの計算だからということでp=0.5-0.6の範囲で行うとcurvefitができない。0.61もNG。0.62はOK、何故NGなのか、プログラムを確認する必要がある。

curveFit_critical_P_v4.pyについて
こちらも同様。p=0.6-0.7はNG、p=0.58-0.7はOK。

forestFire_clusterStructureについて
これも上記と同様にcurveFit_critical_xi_v4.pyは0.6を絡めるとNG。さらにそもそも的にforestFire_clusterSizeで修正を施した「S(w_ave)がpercolation clusterを含んだ計算になっていた」という部分を修正していない。これの修正も今後必要。