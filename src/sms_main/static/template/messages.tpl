% include('template/header.tpl')
<h2>{{table_name}}</h2>
<h3>{{stat}}</h3>


<table>
<tr>
   <td>Recipients</td>
   <td>Message</td>
   <td>Timestamp</td>
   <td>Status</td>
   <td>Action</td>
<tr>

   % for row in rows:
    <tr>
    <td>{{row[1]}}</td>
    <td>{{row[2]}}</td>
    <td>{{row[3]}}</td>
    <td>{{row[4]}}</td>
    <td><a href="{{delete_string}}?id={{row[0]}}">Delete</a></td>
    </tr>
   % end



</table>







