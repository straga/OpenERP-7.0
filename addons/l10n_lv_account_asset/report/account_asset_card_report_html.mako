<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<%import time%>
<% count = 0 %>
%for obj in objects :
    <% setLang(user.lang) %>
	<% count +=1 %>
	%if count > 1 :
	<br/>
	%endif
    <span class="title">${_("PAMATLĪDZEKĻU UZSKAITES KARTĪTE NR. ")}${obj.code}</span>
    <br/>
	<br/>
	<table width=100%>
		<tbody>
			<tr>
				<td colspan="2">${_("Pamatlīdzekļu objekta nosaukums")}</td>
				<td>${_("Kods")}</td>
				<td style="text-align:center;border:thin solid">${obj.code}</td>
				<td>${_("Nolietojuma normas kods")}</td>
				<td style="text-align:center;border:thin solid">${obj.category_id.name}</td>
			</tr>
			<tr>
				<td colspan="2" style="border:thin solid">${obj.name}</td>
				<td colspan="2"></td>
				<td colspan="2"></td>
			</tr>
			<tr>
				<td colspan="2">${_("Atrašanās vieta")}</td>
				<td>${_("Skaits")}</td>
				<td style="border:thin solid;text-align:center">${_("1")}</td>
				<td colspan="2"></td>
			</tr>
			<tr>
				<td colspan="2" style="border:thin solid"></td>
				<td colspan="2"></td>
				<td>${_("Amortizācijas likme gadā, %")}</td>
				<td style="border:thin solid;text-align:right">${"%0.2f" % (((obj.purchase_value/((obj.method_period*obj.method_number)/12))*100)/obj.purchase_value) or ''}</td>
			</tr>
			<tr>
				<td>${_("Nodošanas ekspluatācijā datums")}</td>
				<td style="border:thin solid;text-align:center">${obj.purchase_date}</td>
				<td>${_("Sākotnējā uzskaites vērtība (Ls)")}</td>
				<td style="border:thin solid;text-align:right">${obj.purchase_value}</td>
				<td style="text-align:right">${_("summā (Ls)")}</td>
				<td style="border:thin solid;text-align:right">${"%0.2f" % (obj.purchase_value/((obj.method_period*obj.method_number)/12)) or ''}</td>
			</tr>
			<tr>
				<td>${_("Derīgās lietošanas laiks (gados)")}</td>
				<td style="border:thin solid;text-align:center">${"%0.2f" % ((obj.method_period*obj.method_number)/12) or ''}</td>
				<td>${_("Likvidācijas (lūžņu) vērtība (Ls)")}</td>
				<td style="border:thin solid;text-align:right">${obj.salvage_value}</td>
				<td>${_("Tas pats mēnesī, %")}</td>
				<td style="border:thin solid;text-align:right">${"%0.2f" % (((obj.purchase_value/(obj.method_period*obj.method_number))*100)/obj.purchase_value) or ''}</td>
			</tr>
			<tr>
				<td>${_("Tas pats mēnešos")}</td>
				<td style="border:thin solid;text-align:center">${obj.method_period*obj.method_number or ''}</td>
				<td>${_("Viena mēneša nolietojuma summa (Ls)")}</td>
				<td style="border:thin solid"></td>
				<td style="text-align:right">${_("summā (Ls)")}</td>
				<td style="border:thin solid;text-align:right">${"%0.2f" % (obj.purchase_value/(obj.method_period*obj.method_number)) or ''}</td>
			</tr>
			<tr>
				<td colspan="2"></td>
				<td colspan="2"></td>
				<td colspan="2">${_("Piezīmes ")}</td>
			</tr>
			<tr>
				<td>${_("Izslēgšanas datums")}</td>
				<td style="border:thin solid"></td>
				<td colspan="2"></td>
				<td colspan="2" style="border:thin solid"></td>
			</tr>
			<tr>
				<td colspan="2">${_("un pamatojums")}</td>
				<td colspan="2"></td>
				<td colspan="2" style="border:thin solid"></td>
			</tr>
			<tr>
				<td colspan="2" style="border:thin solid"><font color="white">${_("pamat.")}</font></td>
				<td colspan="2"></td>
				<td colspan="2" style="border:thin solid"></td>
			</tr>
		</tbody>
	</table>
	<br/>
	% if obj.state not in 'draft' :
	<table width="100%" border="1">
		<thead>
			<tr>
				<th rowspan="2" width="8%">${_("Datums")}</th>
				<th rowspan="2">${_("Saimnieciskā darījuma apraksts un dokumenta numurs un datums")}</th>
				<th rowspan="2">${_("Iegādes vai ražošanas pašizmaksa")}</th>
				<th rowspan="2">${_("Rekonstrukcija")}</th>
				<th colspan="2">${_("Pārvērtēšana")}</th>
				<th rowspan="2">${_("Uzskaites vērtība")}</th>
				<th rowspan="2">${_("Nolietojums")}</th>
				<th rowspan="2">${_("Atlikusī vērtība")}</th>
			</tr>
			<tr>
				<th width="10%">${_("pieaugums")}</th>
				<th width="10%">${_("samazinājums")}</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>${obj.purchase_date}</td>
				<td>${_("Pamatlīdzekļa pieņemšana ekspluatācijā")}</td>
				<td style="text-align:right">${obj.purchase_value}</td>
				<td></td>
				<td></td>
				<td></td>
				<td style="text-align:right">${obj.purchase_value}</td>
				<td></td>
				<td style="text-align:right">${obj.purchase_value}</td>
			</tr>
			%for line in obj.depreciation_line_ids :
			%if line.move_check == True :
			<tr>
				<td>${line.depreciation_date}</td>
				<td>${_("Nolietojums")}</td>
				<td style="text-align:right">${line.asset_id.purchase_value}</td>
				<td></td>
				<td></td>
				<td></td>
				<td style="text-align:right">${"%0.2f" % (line.remaining_value + line.amount)}</td>
				<td style="text-align:right">${line.amount}</td>
				<td style="text-align:right">${line.remaining_value}</td>
			</tr>
			%endif
			%endfor
		</tbody>
	</table>
	%endif
	<p style="page-break-after:always"></p>
%endfor
</body>
</html>
