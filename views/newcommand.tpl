{% extends 'base.tpl' %}

{% block content %}
    <div class="row">
    
        <form action="/messages/new" method="POST">
            
            <label for="ident">Ident</label>
            <input type="text" name="ident" placeholder="ident"/>
            
            <label for="command">Command</label>
            <input type="text" name="command" placeholder="example"/>
            
            <label for="data">Command Response</label>
            <textarea name="data" placeholder="example response to a command" rows="3" width="100%"></textarea>
            <input type="submit"/> 
        </form>
    <div>
{%  endblock %}
