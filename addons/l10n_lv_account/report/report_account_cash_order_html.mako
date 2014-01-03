<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<%
	count = 0;
%>
%for obj in objects :
	%for line in obj.report_line_ids :
    <% setLang(user.lang) %>
<%
	count += 1;
%>
	%if count != 1 :
	<br/>
	<br/>	
	%endif
    <span class="title">${line.amount>=0 and _("Kases ieņēmumu orderis ") or _("Kases izdevumu orderis ")}${line.ref or ""}</span>
	<br/>
	<br/>
	<span><b>${line.date}</b></span>
    <br/>
	<br/>
	<br/>
	<br/>
    <table class="list_table" width="100%">
        <thead>
			<tr>
				<th class>${_("Korespondējošā konta nr.")}</th>
				<th class>${_("Analītiskā uzskaites konta nr.")}</th>
				<th class>${_("Naudas vienība")}</th>
				<th class>${_("Summa")}</th>
			</tr>
		</thead>
        <tbody>
        	<tr>
				<td style="text-align:center">${line.account_id.code}</td>
				<td style="text-align:center">${line.analytic_account_id.name or _("-")}</td>
				<td style="text-align:center">${line.company_id.currency_id.symbol}</td>
				<td style="text-align:right">${(line.amount>=0 and line.amount) or 0-line.amount}</td>
			</tr>
        </tbody>
    </table>
	<br/>
	<br/>
<%
amount = line.amount
if line.amount<0:
	amount = 0-line.amount
%>
	<span>${_("Summa vārdiem: ")}${helper.verbose_num_lv(amount, line.company_id.currency_id.name)}</span>
	<br/>
	<br/>
	<span>${line.amount>=0 and _("Pieņemts no: ") or _("Izsniegts: ")}${line.partner_id.name or "__________________________________________"}${_(" p.k. ")}${line.partner_id.ref or "_______________________________"}</span>
	<br/>
	<br/>
	<span>${_("Pamatojums: ")}${line.name}</span>
	<br/>
	<br/>
	<br/>
	<br/>
	<table class="list_table">
		<tbody>
			<tr>
				%if line.amount<0 :
				<td style="border-top:none;text-align:left"><b>${line.amount<0 and _("Vadītājs: _______________________________ ")}</b></td>
				%endif
				<td style="border-top:none;text-align:left"><b>${_("Grāmatvedis: _______________________________ ")}</b></td>
				<td style="border-top:none;text-align:left"><b>${line.amount>=0 and _("Kasieris: _______________________________") or _("Izsniedza kasieris: _______________________________")}</b></td>
			</tr>
		</tbody>
	</table>
	<p style="page-break-after:always"></p>
	%endfor
%endfor
</body>
</html>
