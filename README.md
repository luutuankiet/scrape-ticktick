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


# results
![image](https://github.com/user-attachments/assets/c5eaf63a-02c7-402c-851f-23c5cdb35ff4)

![image](https://github.com/user-attachments/assets/14d7efb0-e3d1-42ff-9e4a-6c556d1304ad)
