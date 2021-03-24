# How to create a release

1. Update [issues](https://github.com/SynBioDex/pySBOL3/issues) and
   [pull requests](https://github.com/SynBioDex/pySBOL3/pulls) so they
   are appropriately targeted for this milestone and closed
1. Tag the release using [semantic versioning](http://semver.org)

   ```shell
   cd <pySBOL3>
   git checkout master
   git tag -a v1.X -m "Release 1.X" master
   git push origin --tags
   ```

1. Update GitHub [milestones](https://github.com/SynBioDex/pySBOL3/milestones)
   * Close the current milestone
   * Create a new milestone for the next release
1. Create source and binary distributions

   ```shell
   # Remove any old builds
   rm -rf dist build sbol3.egg-info
   
   # Build source and binary distributions
   python3 setup.py sdist bdist_wheel
   ```

1. Create a GitHub release, upload the wheel and source tarball
   * [Create a release](https://github.com/SynBioDex/pySBOL3/releases/new) (Releases; Draft a new release)
   * Use the current tag
   * Name it "Major.Minor[.Patch]"
   * Upload the source tar file and the wheel found in `dist`
1. Upload packages to [pypi.org](https://pypi.org/project/sbol3/)

   ```shell
   python3 -m twine upload dist/*
   ```

1. (While in prerelease) Update the default version on [readthedocs](https://readthedocs.org/)
   * Admin -> Advanced Settings
   * Set "Default version" to the newly release alpha version
   * We shouldn't have to do this after the 1.0 release

1. Bump the version numbers on the develop branches
   * _Note: Use the standard contribution process by submitting these
     changes via a pull request on your fork, not a direct push to the
     SynBioDex repository_
   * Bump version number in `setup.py`
   * Bump version number in the `sbol3/__init__.py`
   * Bump version number in `docs/conf.py`
