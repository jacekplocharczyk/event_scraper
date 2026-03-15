import pytest

ZACHETA_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Zacheta Calendar</title>
</head>
<body>
    <ul>
        <li>
            <a href="/pl/kalendarz/wystawka-sztuki-wspolczesnej-123">
                15.03 (PT) 19:00  Modern Perspectives  Sala Główna
            </a>
        </li>
        <li>
            <a href="/pl/kalendarz/warsztaty-malarskie-456">
                20.03 (ND) 15:30  Painting Workshop  Studio B
            </a>
        </li>
        <li>
            <a href="/pl/kalendarz/wykład-historia-sztuki-789">
                25.04 (PT) 18:00  Lecture on Art History
            </a>
        </li>
    </ul>
</body>
</html>
"""


@pytest.fixture
def zacheta_html():
    return ZACHETA_HTML
