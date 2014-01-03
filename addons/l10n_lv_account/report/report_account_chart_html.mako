<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <% setLang(user.lang) %>
    <span class="title">${_("Chart of Accounts")}</span>
    <br/>
    <table class="list_table"  width="90%">
        <thead>
			<tr>
				<th class>${_("Code")}</th>
				<th class>${_("Name")}</th>
				<th class>${_("Internal Type")}</th>
				<th class>${_("Currency")}</th>
				<th class>${_("State")}</th>
			</tr>
		</thead>
		%for a in lines(data['form']) :
        <tbody>
        	<tr>
				<td>${a['code']}</td>
				<td>${a['name']}</td>
				<td>${a['type']}</td>
				<td>${a['currency']}</td>
				<td>${(a['active'] == True and _("Open")) or (a['active'] == False and _("Closed"))}</td>
			</tr>
        </tbody>
		%endfor
    </table>
</body>
</html>
