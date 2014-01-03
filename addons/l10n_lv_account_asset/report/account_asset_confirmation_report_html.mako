<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<% count = 0 %>
%for obj in objects :
	<% setLang(user.lang) %>
	<% count += 1 %>
	%if count > 1 :
	<br/>
	%endif
	<span><b>${_("APSTIPRINU:")}</b></span>
	<br/>
	<span>${_("Vadītājs ________________________")}</span>
	<br/>
	<span>${_("Datums: ________________________")}</span>
	<br/>
	<br/>
	<div class="title" style="text-align:center">${_("AKTS")}</div>
	<div class="title" style="text-align:center">${_("Par pamatlīdzekļu pieņemšanu un ieviešanu ekspluatācijā.")}</div>
	<br/>
	<br/>
	<span><b><u>${_("Materiālās vērtības īss raksturojums:")}</u></b></span>
	<br/>
	<br/>
	<table width="100%" border="1">
		<thead>
			<tr>
				<th width="20%">${_("Nosaukums")}</th>
				<th width="10%">${_("Iegādes vērtība")}</th>
				<th width="15%">${_("Nolietojuma atskaitījuma norma gadā (%) / (Ls) mēnesī")}</th>
				<th width="15%">${_("Ieviešana ekspluatācijā (datums)")}</th>
				<th width="15%">${_("Pilna nolietojuma termiņš (mēnešos)")}</th>
				<th>${_("Piezīmes")}</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>${obj.name}</td>
				<td style="text-align:center">${obj.purchase_value}</td>
				<td style="text-align:center">${"%0.2f" % (((obj.purchase_value/((obj.method_period*obj.method_number)/12))*100)/obj.purchase_value) or ''} / ${"%0.2f" % (obj.purchase_value/(obj.method_period*obj.method_number)) or ''}</td>
				<td style="text-align:center">${obj.purchase_date}</td>
				<td style="text-align:center">${obj.method_period*obj.method_number or ''}</td>
				<td>${obj.note or ''}</td>
			</tr>
		</tbody>
	</table>
	<br/>
	<br/>
	<br/>
	<span><b><u>${_("Apskates dalībnieku sekojošā sastāvā:")}</u></b></span>
	<br/>
	<br/>
	<table width="100%">
		<tr>
			<td style="border-bottom:2px solid"><b>${_("Komisijas priekšsēdētājs")}</b></td>
		</tr>
		<tr>
			<td style="border-bottom:thin solid">${_("Komisijas locekļi:")}</td>
		</tr>
		<tr>
			<td style="border-bottom:thin solid"><font color="white">...</font></td>
		</tr>
		<tr>
			<td style="border-bottom:thin solid"><font color="white">...</font></td>
		</tr>
		<tr>
			<td style="border-bottom:2px solid"><font color="white">...</font></td>
		</tr>
	</table>
	<br/>
	<br/>
	<br/>
	<span><b><u>${_("Apskates dalībnieki konstatēja sekojošo:")}</u></b></span>
	<br/>
	<br/>
	<table width="100%" border="1">
		<tbody>
			<tr>
				<td width="53%">${_("Materiālā vērtība pieņemšanas - nodošanas brīdī atrodas")}</td>
				<td width="47%"></td>
			</tr>
			<tr>
				<td width="53%">${_("Materiālā vērtība tehniskiem noteikumiem atbilst")}</td>
				<td width="47%"></td>
			</tr>
			<tr>
				<td width="53%">${_("Piestrāde ir vai nav vajadzīga; kas tieši:")}</td>
				<td width="47%"></td>
			</tr>
			<tr>
				<td width="53%">${_("Apskates dalībnieku slēdziens:")}</td>
				<td width="47%"></td>
			</tr>
			<tr>
				<td width="53%">${_("Materiālās vērtības papildinājumi")}</td>
				<td width="47%"></td>
			</tr>
		</tbody>
	</table>
	<br/>
	<br/>
	<br/>
	<br/>
	<br/>
	<br/>
	<br/>
	%if count == 1 :
	<br/>
	%endif
	<table width="100%">
		<tbody>
			<tr>
				<td width="55%">${_("Grāmatvedības atzīme par objekta ieviešanu (pārvietošanu)")}</td>
				<td width="45%" style="border-bottom:thin solid"></td>
			</tr>
		</tbody>
	</table>
	<p style="page-break-after:always"></p>
%endfor
</body>
</html>
