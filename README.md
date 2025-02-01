[![CD](https://github.com/luutuankiet/scrape-ticktick/actions/workflows/gh_deploy.yml/badge.svg)](https://github.com/luutuankiet/scrape-ticktick/actions/workflows/gh_deploy.yml)

# prequisite

- `app/ETL/loader.py` must be initially executed to scaffold json files under `app/ETL/raw`
- after running loader.py the `env` dir should look like so. 

```
app/env
├── .gitkeep
├── .secrets
├── service_account.json
└── .token-oauth
```

- clone ticktick-py-dbt repo with `git clone https://github.com/luutuankiet/ticktick-py-dbt.git`


