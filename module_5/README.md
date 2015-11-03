## Setup on OSX with brew and pip

```brew install python3
sudo pip3 install --upgrade pip setuptools
pip3 install theano matplotlib```

## Locale

The following error

```python
ValueError: unknown locale: UTF-8
```

is solved by adding

```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

to your shells rc-file (i.e. `.bashrc` or `.zshrc`)
