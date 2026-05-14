from chirp import ShellAction, ShellActions, ShellActionZone


def context():
    return {
        "shell_actions": ShellActions(
            primary=ShellActionZone(
                items=(
                    ShellAction(
                        id="fs-workspace-new",
                        label="New workspace run",
                        href="/workspace/new",
                        variant="primary",
                    ),
                )
            ),
            controls=ShellActionZone(
                items=(
                    ShellAction(
                        id="fs-workspace-refresh",
                        label="Refresh",
                        action="refresh-fs-workspace",
                        variant="secondary",
                    ),
                )
            ),
        )
    }
