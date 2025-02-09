(development-reference)=
# Development

Notes for developers. If you want to get involved, please do!


## Contributing

All contributions are welcome, some possible suggestions include:

- tutorials (or support questions which, once solved, result in a new tutorial :D)
- blog posts
- improving the documentation
- bug reports
- feature requests
- pull requests

Please report issues or discuss feature requests in the [SCMData issue tracker](https://github.com/openscm/scmdata/issues).
If your issue is a feature request or a bug, please use the templates available, otherwise, simply open a normal issue.

As a contributor, please follow a couple of conventions:

- Create issues in the [SCMData issue tracker](https://github.com/openscm/scmdata/issues) for changes and
   enhancements, this ensures that everyone in the community has a chance to comment
- Be welcoming to newcomers and encourage diverse new contributors from all backgrounds: see the
   [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/)
- Only push to your own branches, this allows people to force push to their own branches as they need without
   fear or causing others headaches
- Start all pull requests as draft pull requests and only mark them as ready for review once they've been
   rebased onto master, this makes it much simpler for reviewers
- Try and make lots of small pull requests, this makes it easier for reviewers and faster for everyone as
   review time grows exponentially with the number of lines in a pull request

## Getting setup

To get setup as a developer, we recommend the following steps:

- Install conda, make and poetry
- Run `make virtual-environment`, if that fails you can try running the steps in the Makefile manually
- Make sure the tests pass by running `make test-all`


## Language

We use British English for our development.
We do this for consistency with the broader work context of our lead developers.

## Docstring style

For our docstrings we use numpy style docstrings.
For more information on these, [here is the full guide](https://numpydoc.readthedocs.io/en/latest/format.html)
and [the quick reference])https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html) is
also useful.


## Versioning

This package follows the version format described in [PEP440](https://peps.python.org/pep-0440/) and
[Semantic Versioning](https://semver.org/) to describe how the version should change depending on the updates to the
code base. Our commit messages are written using written to follow the
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) standard which makes it easy to find the
commits that matter when traversing through the commit history.

(releasing-reference)=
## Releasing

Releasing is semi-automated via a CI job. The CI job requires the type of version bump that will be performed to be
manually specified. See the poetry docs for the [list of available bump rules](https://python-poetry.org/docs/cli/#version).

### Standard process

The steps required are the following:


1. Bump the version: manually trigger the "bump" workflow from the main branch
   (see here: https://github.com/openscm/scmdata/actions/workflows/bump.yaml).
   A valid "bump_rule" (see https://python-poetry.org/docs/cli/#version) will need to be specified.
   This will then trigger a draft release.

1. Edit the draft release which has been created
   (see here:
   https://github.com/openscm/scmdata/releases).
   Once you are happy with the release (removed placeholders, added key
   announcements etc.) then hit 'Publish release'. This triggers a release to
   PyPI (which you can then add to the release if you want).


1. That's it, release done, make noise on social media of choice, do whatever
   else

1. Enjoy the newly available version

## Read the Docs

Our documentation is hosted by
[Read the Docs (RtD)](https://www.readthedocs.org/), a service for which we are
very grateful. The RtD configuration can be found in the `.readthedocs.yaml`
file in the root of this repository. The docs are automatically
deployed at
[scmdata.readthedocs.io](https://scmdata.readthedocs.io/en/latest/).
