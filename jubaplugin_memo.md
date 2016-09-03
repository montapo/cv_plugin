# 画像特徴量抽出plugin 自分用memo

## jubatus関連
- edge vision plug-in by kumagi : https://github.com/jubatus/edge_vision_api/tree/master/jubatus_plugin
- jubatusプラグイン開発ガイド : K開発の中にあり \\KFSS-SVR00.iecl.ntt.co.jp\FS_I2P_share\I二P\I基D\個別案件関連\K開発\040-references
- fv_converter開発手順 : http://jubat.us/ja/plugin.html
- 特徴抽出/バイナリのインターフェース : https://github.com/jubatus/jubatus_core/blob/master/jubatus/core/fv_converter/binary_feature.hpp
- バイナリ型特徴抽出
>バイナリ型のデータに対する特徴抽出を経て生成される特徴ベクトルの各次元の名称は、プラグインが任意に指定することができるため、衝突が発生しないよう設計する必要がある。

    ```
    /**
    * @param[in] key Datum の binary_values 登録された Key 名
    * @param[in] value Datum の binary_values に登録された値
    * @param[out] ret_fv 特徴抽出の結果 (Key-Value で表現される特徴ベクトル)
    */
    virtual void add_feature(
        const std::string& key,
        const std::string& value,
        std::vector<std::pair<std::string, float> >& ret_fv) const = 0;

    ```
- 作ったプラグインを使う方法 : 
    - config をjson形式で書く
    ```
    {
    "method": "perceptron",
    "converter": {
        "string_filter_types": {},
        "string_filter_rules": [],
        "num_filter_types": {},
        "num_filter_rules": [],
        "string_types": {},
        "string_rules": [],
        "num_types": {},
        "num_rules": [],
        "binary_types":{
        "length": {
            "method": "dynamic",
            "path": "/path/to/libbinary_length.so",
            "function": "create"
        }
        },
        "binary_rules": [
        {"key" : "*", "type" : "length"}
        ],
        "combination_types": {},
        "combination_rules": []
    }
    }
    ```
- `binary_types`と`binary_rules`に詳細を記述してやる
    - `binary_types`:特徴抽出に"length"を用いる
        - `method` : dynamic - **plugin**を使用
        - `path` - ライブラリがある場所を指定
        - `function` - 呼び出し関数名(externで記述したやつ)
    - `binary_rules`:特徴抽出の適用規則を定義
        - `key` : 適用対象とするDatumのkey名
        - `type` : length - `binary_types`で定義した手法の名前
---    
## C++関連
- 純粋仮想関数(プロトタイプ宣言) : http://kaworu.jpn.org/cpp/%E7%B4%94%E7%B2%8B%E4%BB%AE%E6%83%B3%E9%96%A2%E6%95%B0
    >いずれかの時点で必ずオーバーライド(関数の再定義)をしてやらなければならない
- extern,コンパイルとリンク : http://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14147907649
- 参照渡し : アドレスを渡す。値ではない http://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q149903394
- `rdbuf` : http://mattn.kaoriya.net/software/lang/c/20110402011210.html
- scoped_ptrとshared_ptrのちがい : ????
- デストラクタにvirtualをつけるとき http://qiita.com/ashdik/items/3cb3ee76137d176982f7
    - コンストラクタの順番 : 基底クラス⇒メンバ⇒自身の本体
    - デストラクタの順番 : 本体⇒メンバ⇒基底クラス
    - 子クラスのポインタを親クラスのポインタにキャストして使用するならデストラクタはvirtual
    ```
    class Parent {
        //デストラクタにvirtualを書く
        ...};
    class Child : public Parent {
        ...
        };
    Parent* parent = new Child()
    ```
    - virtual : 子クラスのポインタは必ず親クラスのポインタとして使用される⇒
    子クラスの存在に気づかずメモリリークするのを防ぐ
- コマンドライン引数の使い方 http://www9.plala.or.jp/sgwr-t/c/sec11-4.html
    - argv[0]にはコマンド自体(実行コマンドが`./a.out`なら`argv[0]==/a.out`)
- istreamとifstream
    - stream処理には>>演算子を使うことが多い
    - istream : データ列の入力(ファイルに限らない)に使う
    - ifstream : ファイルの入力に使う `std::ifstrea, << ifs(arg[1]);` 
    - ifstream::noskipws
- std::copyの使い方 : `std::copy(first, end, result);`
- stream iterator の使い方 : http://ppp-lab.sakura.ne.jp/cpp/library/014.html
    - 例

    ```
    int main()
    {
        using namespace std;

        ostream_iterator<int> oit( cout, "\n" ); // coutストリーム用のostream
        *oit = 10;  // 10を出力し"\n"を出力
        *oit = 20;  // 20を出力し"\n"を出力
        *oit = 30;  // 30を出力し"\n"を出力

        return 0;
    }
    ```

    ```
    #include <iostream>
    #include <iterator>

    int main()
    {
        using namespace std;

        istream_iterator<int> iit( cin ); // cinストリーム用のistream
        istream_iterator<int> iit_eof;    // end-of-streamイテレータ

        while( iit != iit_eof )  // EOFかエラーで終了
        {
            cout << *iit << endl;  // １つ読み取って出力
            ++iit;                 // 次の値を読み取る
        }
        return 0;
    }
    ```
- back_inserter : 指定されたコンテナーの後ろに要素を挿入できる反復子を作成.iteratorとあわせ使う？
- `#include <header.h>`と記述したときは，これらのディレクト リからヘッダファイルを探すが，
`include "header.h"`と記述したときは カレントディレクトリをまず探し，その後でこれらのディレクトリから探す．
- const周り
>void hoge(const int a, int b) const; ･･･ 書き換えられない : a, そのクラス内のメンバ変数/書き換えられる : b　


---

## opencv
- 参考 : http://opencv.jp/opencv-2.1/cpp/reading_and_writing_images_and_video.html
- opencvでsurfとかsiftってできない？？
    - http://opencv.jp/opencv2-x-samples/surf_extraction これ昔の実装。動かなかった(surf is no menber of cv)
    - <opencv2/nonfree>とゆうところにヘッダが移されたっぽい？
    - http://kesin.hatenablog.com/entry/20120810/1344582180 　マックで動かしてる
    - http://cfi.iitm.ac.in/ask/question/118/how-do-i-install-nonfree-modules-in-opencv/
        - 特許関連であえて使えなくしているっぽいので、jubatusには組み込まないほうがヨサゲ
        ```
        ~/juba_develop/cv_plugin   ᐅ sudo -E add-apt-repository ppa:xqms/opencv-nonfree  
        Build of OpenCV including the nonfree packages.

        Please be aware of potential patent issues when using this PPA. For a list of included algorithms see:
        http://docs.opencv.org/modules/nonfree/doc/nonfree.html
        詳しい情報: https://launchpad.net/~xqms/+archive/ubuntu/opencv-nonfree
        [ENTER] を押すと続行します。ctrl-c で追加をキャンセルできます

        ```
    - surfじゃなくてorbがいいよ:http://ishidate.my.coocan.jp/opencv_10/opencv_10.htm
    - 局所特徴量の初心者向けslide : http://www.slideshare.net/lawmn/siftsurf
    - SIFTとそれ以降のアプローチ : http://www.slideshare.net/hironobufujiyoshi/miru2013sift0
- このへんにHOG書いてる？? 
    - https://github.com/opencv/opencv/blob/26bf5b5de307d1db0994eb825697f0c2b42c7269/modules/objdetect/include/opencv2/objdetect.hpp#L337-L454
    - https://github.com/opencv/opencv/blob/26bf5b5de307d1db0994eb825697f0c2b42c7269/modules/objdetect/src/hog.cpp#L1582-L1644
- opencv3
    - いんすこ：http://umejan.hatenablog.com/entry/2016/04/20/233642
    - なんか怒られた
    ```
    /usr/bin/ld: -lippicv が見つかりません
    collect2: error: ld returned 1 exit status
    ```
        - 解決策？http://kivantium.hateblo.jp/entry/2016/04/08/230302
        

---

## 画像 LBPとHOGを実装したいー
- 中山先生のBoF 
    - http://d.hatena.ne.jp/n_hidekey/20111120/1321803326
    - http://d.hatena.ne.jp/n_hidekey/20120204/1328363973
- LBPの実装 http://suzuichibolgpg.blog.fc2.com/blog-entry-285.html
- HOGの実装 http://qiita.com/kooh-z/items/3e3f85e93d894b4645f7#hog%E7%89%B9%E5%BE%B4%E9%87%8F%E3%81%A8%E3%81%AF
- dlibのLBP http://dlib.net/dlib/image_transforms/lbp_abstract.h.html#extract_uniform_lbp_descriptors
---

## 環境構築
- kumagi : dlibが必要
- unnounno : opencvが必要
- Opencvとdlibのインストール
    - http://yamaguchi-1024.hatenablog.com/entry/2015/11/13/164814
        - opencvムリだった。
    - http://vaaaaaanquish.hatenablog.com/entry/2016/06/28/004811
    - dlib:コンパイルできない。はまった。
        - 解決？？http://qiita.com/ryohey/items/aeb6bfdbc135ce020f02
- Opencvとdlibのインストール
    - dlibを用いた顔認識 : http://yamaguchi-1024.hatenablog.com/entry/2015/11/13/164814
        - opencvムリだった。
    - opencvとdlibを使ってみた : http://vaaaaaanquish.hatenablog.com/entry/2016/06/28/004811
    - opencvをubuntu14.04に入れる方法 : http://shumilinux.blogspot.jp/2015/08/ubuntu-1404-lts-opencv.html
    - opencv : 必要なライブラリ群が書いてある : http://www.icrus.org/horiba/article/2014_11_07_01.php

    ```    
    sudo apt-get -y install build-essential libgtk2.0-dev libjpeg-dev libtiff4-dev libjasper-dev libopenexr-dev cmake python-dev python-numpy python-tk libtbb-dev libeigen3-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev default-jdk ant libvtk5-qt4-dev    
    ``` 
    - `sudo apt-get install libopencv-dev`でok
    - dlib:コンパイルできない。はまった。
        - きちんとコンパイルできればOK
        - stack overflow : 
- /usr/localって何？ http://hateda.hatenadiary.jp/entry/2014/02/02/191807

---

## ???
- プロトタイプ宣言とリンケージ
- C++の継承の書き方
    - virtual?? ポリもーフィズ無？？？
- .soファイル(shared object)
    - unix系OSの共有ライブラリのファイル形式. ほかのプログラムにリンクしてその帰納を呼び出すようになっている
    - windowsでは.DLLらしい
    - 共有ライブラリとは、複数のプログラムが共通して使うライブラリ
    - ダイナミックリンクのライブラリで、プログラム時にリンクが行われる
    - 一方でstatic linkはビルド時にリンクが行われる。(拡張子は.a)
- liblog4cxxとは
- hogehoge_factory.hpp/cpp とは
- `lexical_cast`
- `->,>>`など
- /usr/localって何？ http://hateda.hatenadiary.jp/entry/2014/02/02/191807
- バッファって何？ http://oshiete.goo.ne.jp/qa/8314022.html
---