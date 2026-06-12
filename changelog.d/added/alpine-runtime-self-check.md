Added a client-side Alpine runtime self-check to `chirpui-alpine.js`: when
chirp-ui components that require Alpine render but Alpine never initializes (a missing,
blocked, or misconfigured CDN script; a CSP block; a network error; or
`alpine=False`), the runtime now logs a loud `console.warn` with the likely
causes instead of leaving every interactive component silently inert. The
end-to-end Alpine-liveness proof (`tests/browser/test_alpine_lifecycle.py`,
including the new silent-disable case) is now wired into the
`test-browser-chrome` gate, and a Vitest unit test covers the self-check logic
in the fast `poe ci` suite ([#189](https://github.com/lbliii/chirp-ui/issues/189), [#190](https://github.com/lbliii/chirp-ui/issues/190)).
