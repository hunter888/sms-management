% include('template/header.tpl')

<h2>Bulk Messaging</h2>
<h3>{{stat}}</h3>

<h4> Note: Uploaded file must be in csv format and looks like below:</h4>
<p>
09172324223,This is a message<br>
09172324223,<br>
09172324223,Another message<br>
09172324223,<br>
</p>

<h4> Note: Item with empty message will use the default message below:</h4>
<form action="/create_bulk_message" method="post"  enctype="multipart/form-data">
    Recipients: <input name="upload" type="file" />
    <br>
    <br>
    Default Message: 
    <textarea id="message" name="message" rows="5" cols="70"></textarea>
    <br>
    <br>
    <input value="Send" type="submit" />
</form>


<br>
<table>
<tr> <th>Recipient</th> <th>Message</th>
% for row in data:
    <tr>
    <td> {{row[0]}}</td>
    <td> {{row[1]}}</td>
    </tr>
%end


</table>










