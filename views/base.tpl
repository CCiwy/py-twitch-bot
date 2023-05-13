{% from './macros/navigation.macro' import navigation_links with context %}
{# get template context #}
{% set get_url = template_context["get_url"] %}
<html>
    <head>
        <title>Debug Title</title>
    </head>

    <link rel="stylesheet" href="/static/skeleton.css" type="text/css">
    <link rel="stylesheet" href="/static/normalize.css" type="text/css">
    <link rel="stylesheet" href="/static/styles.css" type="text/css">
    <body>
        {% set navigation = template_context["navigation"] %}
        {{ navigation_links(navigation, get_url) }}
        <hr>
        <main>

        {% block content %}

        {% endblock %}
        </main>

        <br>
        
        <hr>
    </body>
    <footer>
    BASE TPL FOOTER
</footer>
</html>
