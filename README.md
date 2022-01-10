# 概要
- マッチングアプリに自動で足跡をつける
- 足跡のうち、いいね未送信のユーザーに対していいねを送信する

# 使用方法

```bash
# コンテナ起動
docker-compose up -d
# 足跡を付ける
docker-compose run --rm app python -m scraping.main
# 足跡のうちlikeを送っていないユーザーにlikeを送信する
docker-compose run --rm app python -m scraping.like
```

## notebookを使用する場合

```bash
# コンテナを起動し、bash実行
docker-compose run --rm app bash
# コンテナ内でjupyterlabを起動する
jupyter-lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=''
```

## formatter
```python
docker-compose run --rm app make
```
