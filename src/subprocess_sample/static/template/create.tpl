% include('template/header.tpl')

<h2>Write Message</h2>
<h3>{{stat}}</h3>

<form action="/create_message" method="post">
    Recipients: <input name="recipients" type="text" />
    <br>
    <br>
    Message: 
    <textarea id="message" name="message" rows="5" cols="70"></textarea>
    <br>
    <br>
    <input value="Send" type="submit" />
</form>
