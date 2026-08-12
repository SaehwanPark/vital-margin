# Contributor Release Metadata Check

The repository has one lightweight release-readiness check for the package
version projections. Run it from the repository root:

```bash
python3 scripts/check_release_metadata.py
```

The check compares the modified `x.y.z` package version in `Cargo.toml` with:

- the `vital-margin` package entry in `Cargo.lock`;
- the public milestone line in `README.md`; and
- the first version heading in `CHANGELOG.md`.

It is read-only and has no dependency on Rust execution, simulation state,
scenario data, replay artifacts, registries, tags, package publication, or
deployment. The same command runs in `.github/workflows/ci.yml`.

When changing the package version, update the lockfile, README, changelog, and
`SPEC.md` according to [`docs/reference/versioning-policy.md`](../reference/versioning-policy.md),
then run this check before opening a pull request.

This metadata check is one part of the broader source-checkout decision. For
the required checkout contents, runtime support boundaries, and the complete
read-only validation sequence, see [Reproducible Distribution](reproducible-distribution.md).
