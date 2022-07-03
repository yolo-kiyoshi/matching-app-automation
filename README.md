# 概要
- マッチングアプリに自動で足跡をつける
- 足跡のうち、いいね未送信のユーザーに対していいねを送信する

# 使用方法

```bash
# コンテナ起動
docker-compose up
# 足跡のうちlikeを送っていないユーザーにlikeを送信する
docker-compose run --rm scraping python -m scraping.like
```

## formatter
```python
docker-compose run --rm scraping make
```
