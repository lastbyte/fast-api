# GETTING STARTED WITH fastAPI

## Setting up the environment

### cloning the repo

#### clone the repository using the following command

- if you are using ssh
    ```bash
    git clone git@github.com:lastbyte/fast-api.git
    ```

- still on https use
    ```bash
    git clone https://github.com/lastbyte/fast-api.git
    ```

#### setting up the environment variables

using the template file named `.env.example`, create a file named `.env`

the content of the env file looks like

```
APP_ENV=dev
APP_PORT=8000
JWT_TOKEN_SECRET=*********

DB_USER=postgres
DB_PASSWORD=********
DB_HOST=127.0.0.1
DB_POST=5432
DB_NAME=web

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_KEY=****************
```

populate the files with the correct set of values.


#### Setting up the dependencies

create a virtual environment for development and install the dependencies using the command

```bash
pip install -r requirements.txt
```


#### Running the app

Head to VS Code and open the `debug and run` pane. and start the Application using the `Launch App` run configuration.

