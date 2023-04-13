# SQLITE3 on Raspberry Pi

By default, python on my Raspberry Pi does not have sqlite3 installed.

I have tried the following to install it, with no success:

## Install sqlite3

```bash
sudo apt-get install sqlite3
```

## Install sqlite3-dev & rebuild python

```bash
sudo apt-get update
sudo apt-get install libsqlite3-dev
cd ~/Python-3.11.0
./configure --enable-loadable-sqlite-extensions && make && sudo make install
```
