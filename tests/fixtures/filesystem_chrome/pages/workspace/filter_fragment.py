from chirp.http.response import Response


def get():
    return Response(
        '<section class="chirpui-block" data-testid="fs-filter-result">'
        "<h2>Filtered filesystem workspace</h2>"
        "<p>Local fragment returned without shell or page-root wrappers.</p>"
        "</section>"
    )
