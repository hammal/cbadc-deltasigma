# cbadc-deltasigma

A maintained fork of [python-deltasigma](https://github.com/ggventurini/python-deltasigma) for the optional delta-sigma synthesis tools in [cbadc](https://github.com/hammal/cbadc). The fork updates compatibility with current Python, NumPy, and SciPy releases and is published separately from cbadc.

```sh
pip install cbadc-deltasigma
```

```python
import cbadc_deltasigma as ds

ntf = ds.synthesizeNTF(3, 32)
```

The PyPI distribution is `cbadc-deltasigma`; its Python import is `cbadc_deltasigma`. It is distinct from the original `deltasigma` package and can coexist with it.

This fork descends from work by Richard Schreier, Giuseppe Venturini, Sergio Callegari, Yuki Fukuda, and other contributors. Copyright notices and the BSD-style redistribution terms are in [LICENSE](LICENSE). See [RELEASING.md](RELEASING.md) for the release process.
