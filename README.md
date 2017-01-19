# IbPy - Interactive Brokers Python API

## NOTE

Beginning with release 9.73, InteractiveBrokers is now officially supporting a new Python API client (Python 3 only).
This should make this repo superfluous except for Python 2.

For more info: https://interactivebrokers.github.io/tws-api/#gsc.tab=0

## What is IbPy?

IbPy is a third-party implementation of the API used for accessing the
Interactive Brokers online trading system. IbPy implements functionality that
the Python programmer can use to connect to IB, request stock ticker data,
submit orders for stocks and futures, and more.

## Installation

There is a package maintained on PyPI under the name IbPy2, it's version is in sync
with the tags on GitHub.

```
pip install IbPy2
```

Alternatively, it can be installed from source. From within the IbPy directory, execute:

```
python setup.py install
```

Pip also supports installing directly from GitHub, e.g. if you want commit `83b9d08ed9c850d840a6700d0fb9c3ca164f9bff`, use

```
pip install git+https://github.com/blampe/IbPy@83b9d08ed9c850d840a6700d0fb9c3ca164f9bff
```

## How do I use IbPy?

See the IbPy wiki page https://github.com/blampe/IbPy/wiki/Getting-Started

## What are the requirements?

* Python >2.5 or >3.3. Previous versions are not supported.
* Either a running instance of Trader Workstation (TWS) or IB Gateway.

## License

IbPy is distributed under the New BSD License. See the LICENSE file in the
release for details.

## Note

IbPy is not a product of Interactive Brokers, nor is this project affiliated
with IB.

## Source code

https://github.com/blampe/IbPy