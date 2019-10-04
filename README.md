# BigQuery Profiler

Google BigQueryに任意のSQLクエリを発行し、その結果の統計情報を取得します。
モードは次の3つがあります。

* DataFrame Describe
* BigQuery SQL
* Pandas Profiling

選択できる出力先はモードにより異なりますが、CSV、BQテーブル、HTMLがあります。
ファイルの場合は`gs://~`にも対応しています。

# インストール方法

次のようにインストールできます。
`bq_profile`スクリプト中では`docker run ... colorfulboard/bq_profile:latest ...`を実行しています。

```shell
$ curl https://gist.githubusercontent.com/rhoboro/9c27090715205b8e54c73590830e1b7c/raw/da254ae9bffcadbb564ef3cbb57a2fb7be98617e/bq_profile > bq_profile
$ chmod +x bq_profile
$ mv bq_profile /usr/local/bin
```

# 使い方

こんなコマンドを実行すると、クエリ結果の統計情報がBQ上に書き込まれます。

```shell
$ bq_profile local \
  --sql "SELECT * FROM my.table WHERE _PARTITIONTIME = TIMESTAMP('2019-10-02')" \
  --project my-project \
  --output-table my.stats \
  --disposition append \
  --mode sql
```

モードによらず共通のオプションは次のとおりです。

* `local`: 実行時にGCP認証情報(`~/.config/gcloud`)をマウントします。
* `--sql`: クエリ文字列かそれを記述したファイルパス
* `--project`: GCPのプロジェクトID
* `--mode[default: describe]`: `describe`,`pandas-profiling`,`sql`のいずれかです

## 認証情報に関して

GCPの認証情報を利用します。

ローカルで個人のユーザアカウントの認証情報を利用する際は `bq_profile local ...` と`local`キーワードを入れてください。
GCEインスタンス上などのGCPのサービスアカウントの認証情報を利用する際は`local`は不要です。

現時点ではJSON形式の認証情報は未サポートです。

## 統計情報の取得

次の3つのモードから選択できます。

* DataFrame Describe
* BigQuery SQL
* Pandas Profiling

データ型はクエリ結果に依存するため、変更したい場合はクエリでキャストしてください。

### DataFrame Describe

* `--output`: アウトプットファイルパス。`gs://`もOK。

### BigQuery SQL

* `--output`: アウトプットファイルパス。`gs://`もOK。
* `--output-table`: `dataset.table`形式のBQテーブル名。`--output`よりも優先される。
* `--disposition`: `--output-table`が既に存在する場合の動きを指定します。`fail`,`replace`,`append`のいずれかです。

### Pandas Profiling

* `--output`: アウトプットファイルパス。`gs://`もOK。

# アップグレード

新しいバージョンがある場合は、`upgrade`コマンドでアップデートします。

```shell
$ bq_profile upgrade
updating...
done
```
