# Publishing cbadc-deltasigma

The release workflow tests Python 3.11–3.15 on Linux, macOS, and Windows,
builds the package, then uploads to PyPI through Trusted Publishing. No PyPI
token is stored in GitHub.

## One-time setup

1. In the GitHub repository settings, create an environment named `pypi`. Require a maintainer's approval for deployments to this environment.
2. In your PyPI account, open **Publishing** and add a **pending GitHub publisher** with these exact values:

   | Field | Value |
   | --- | --- |
   | PyPI project name | `cbadc-deltasigma` |
   | GitHub owner | `hammal` |
   | Repository | `cbadc-deltasigma` |
   | Workflow filename | `release.yml` |
   | Environment name | `pypi` |

The pending publisher does not reserve the project name. The first successful upload creates the project. See [PyPI's pending publisher instructions](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).

## Each release

1. Update the version in `setup.py` and `cbadc_deltasigma/__init__.py`.
2. Let the tests and build on `master` pass.
3. Publish a GitHub release with a tag matching the version, for example `v0.2.6`. That starts the same tests and build; the `pypi` environment then requests approval before the upload.
