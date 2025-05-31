<!DOCTYPE html>
<html>
<head>
    <title>Schülerübersicht</title>
</head>
<body>
    <h1>📋 Schülerakte</h1>
    <ul>
        {% for s in schueler %}
            <li>
                <strong>{{ s.name }}</strong> – {{ s.progress }}
            </li>
        {% endfor %}
    </ul>

    <a href="/start">Zurück zur Startseite</a>
</body>
</html>
