<html>
    <head>
        <title>Debug Title</title>
    </head>

    <body>
        <nav>
            <div>
                {% set navigation = template_context["navigation"] %}
                {% set get_url = template_context["get_url"] %}
                {% for plugin_name, endpoint in navigation.items() %}
                    <div>
                        <a href="{{get_url(endpoint, "health")}}"> {{ plugin_name }} </a>
                    </div>
                {% endfor %}
            </div>
        </nav>
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
