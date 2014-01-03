<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
%for obj in objects :
	<% setLang(user.lang) %>
	<div class="title" style="text-align:center">${_("Kases slēgums: ")}${obj.name}</div>
	<div class="title" style="text-align:center">${obj.date}</div>
	<div class="title" style="text-align:center">${_("Kase: ")}${obj.journal_id.name}</div>
	<br/>
	<br/>
	<div style="text-align:right"><b>${_("Atlikums dienas sākumā: ")}${"%0.2f" % (obj.balance_start)}</b></div>
	<table border="1" width="100%">
		<thead>
			<tr>
				<th class>${_("Ordera Nr.")}</th>
				<th class>${_("No kā saņemts vai kam izsniegts")}</th>
				<th class>${_("Ieņēmumi, LVL")}</th>
				<th class>${_("Izdevumi, LVL")}</th>
			</tr>
		</thead>
		<tbody>
<%
income = 0
expense = 0
%>
	%for line in obj.line_ids :
			<tr>
				<td>${line.ref or ''}</td>
				<td style="text-align:center">${line.partner_id.name or ''}</td>
				<td style="text-align:right">${(line.amount>=0 and line.amount) or ''}</td>
				<td style="text-align:right">${(line.amount<0 and 0-line.amount) or ''}</td>
			</tr>
<%
if line.amount >= 0 :
	income += 1

if line.amount < 0 :
	expense += 1
%>
	%endfor
		</tbody>
	</table>
	<div style="text-align:right"><b>${_("Apgrozījums: ")}${"%0.2f" % (obj.total_entry_encoding)}</b></div>
	<div style="text-align:right"><b>${_("Atlikums dienas beigās: ")}${"%0.2f" % (obj.balance_end)}</b></div>
	<br/>
	<br/>
	<table width="100%">
		<tr>
			<td width="50%"></td>
			<td width="30%" style="text-align:right"><b>${_("Kasieris:")}</b></td>
			<td width="20%"></td>
		</tr>
		<tr>
			<td width="50%"><b>${_("Ieraksti kases grāmatā tika pārbaudīti un saņemti:")}</b></td>
			<td width="30%"></td>
			<td width="20%"></td>
		</tr>
		<tr>
			<td width="50%"><b>${_("ieņēmumu orderi - ")}${income}</b></td>
			<td width="30%"></td>
			<td width="20%"></td>
		</tr>
		<tr>
			<td width="50%"><b>${_("izdevumu orderi - ")}${expense}</b></td>
			<td width="30%"></td>
			<td width="20%"></td>
		</tr>
		<tr>
			<td width="50%"></td>
			<td width="30%" style="text-align:right"><b>${_("Grāmatvedis:")}</b></td>
			<td width="20%"></td>
		</tr>
	</table>
	<p style="page-break-after:always"></p>
%endfor
</body>
</html>
