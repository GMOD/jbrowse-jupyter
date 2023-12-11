## Publishing

General publishing involves creating a new tag

```bash
# e.g.
git tag v1.2.3
git push --tags
```

And then going to https://github.com/GMOD/jbrowse-jupyter/tags and doing "create
release" from the new tag. Then a github action will automatically create the
tags
