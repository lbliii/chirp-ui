from chirp import ShellAction, ShellActions, ShellActionZone


def context():
    return {
        "shell_actions": ShellActions(
            primary=ShellActionZone(
                items=(
                    ShellAction(
                        id="fs-admin-invite",
                        label="Invite admin",
                        href="/admin/invite",
                        variant="primary",
                    ),
                )
            ),
            controls=ShellActionZone(
                items=(
                    ShellAction(
                        id="fs-admin-audit",
                        label="Audit",
                        href="/admin/audit",
                        variant="secondary",
                    ),
                )
            ),
        )
    }
