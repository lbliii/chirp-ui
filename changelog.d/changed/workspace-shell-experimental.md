Demoted `workspace_shell` from `stable` to `experimental` maturity to match the
new [Application Chrome Posture ADR](docs/decisions/application-chrome-posture.md):
the blessed application-chrome composite is the route-context rail wired into
`app_shell`, not the broader workbench *frame*, which the application-chrome plan
still defers. The macro itself is unchanged and continues to render; only its
stability signal (manifest, `chirp-ui find`, generated docs) moves to experimental,
aligning it with `composer_shell` and `dock`.
