<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <% setLang(user.lang) %>
	<span class="title">${_("Pamatlīdzekļu apgrozījums ")}</span>
	<span>${_("no ")}${data['form']['from_date']}</span>
	<span>${_("līdz ")}${data['form']['to_date']}</span>
	<br/>
	<br/>
	<table class="list_table"  width="100%">
		<thead>
			<tr>
				<th colspan="3" class>${_("Operācija")}</th>
				<th class>${_("Uzskaites vērtība")}</th>
				<th class>${_("Nolietojums")}</th>
				<th class>${_("Atlikusī vērtība")}</th>
			</tr>
		<thead>
		<tbody>
<%
	purchase_total_amount_1 = 0.0;
	purchase_total_amount_2 = 0.0;
	purchase_total_amount_3 = 0.0;
	depr_total_amount_1 = 0.0;
	depr_total_amount_2 = 0.0;
	depr_total_amount_3 = 0.0;
	left_total_amount_1 = 0.0;
	left_total_amount_2 = 0.0;
	left_total_amount_3 = 0.0;
%>
			%for asset in lines(data['form']) :
			<tr>
				<td style="border-top:none"><b>${asset['account_code']}</b></td>
				<td style="border-top:none"><b>${asset['account_name']}</b></td>
			</tr>
			<tr>
				<td></td>
				<td colspan="2">${_("Sākuma atlikumi")}</td>
				<td style="text-align:right">${"%0.2f" % (asset['purchase1'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['depr1'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['left1'])}</td>
			</tr>
			<tr>
				<td></td>
				<td colspan="2">${_("Iegāde")}</td>
				<td style="text-align:right">${"%0.2f" % (asset['purchase2'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['depr2'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['left2'])}</td>
			</tr>
			<tr>
				<td></td>
				<td colspan="2">${_("Pamatlīdzekļu nolietojums")}</td>
				<td style="text-align:right">${"%0.2f" % (asset['purchase3'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['depr3'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['left3'])}</td>
			</tr>
			<tr>
				<td></td>
				<td colspan="2">${_("Likvidācija")}</td>
				<td style="text-align:right">${"%0.2f" % (asset['purchase4'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['depr4'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['left4'])}</td>
			</tr>
			<tr>
				<td>${_("Kopā:")}</td>
				<td>${asset['account_code']}</td>
				<td>${_("Kopējā izmaiņa:")}</td>
				<td style="text-align:right">${"%0.2f" % (asset['purchase_total1'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['depr_total1'])}</td>
				<td style="text-align:right">${"%0.2f" % (asset['left_total1'])}</td>
			</tr>
			<tr>
				<td style="border-style:none" colspan="2"></td>
				<td style="border-style:none">${_("Perioda beigās:")}</td>
				<td style="border-style:none;text-align:right">${"%0.2f" % (asset['purchase_total2'])}</td>
				<td style="border-style:none;text-align:right">${"%0.2f" % (asset['depr_total2'])}</td>
				<td style="border-style:none;text-align:right">${"%0.2f" % (asset['left_total2'])}</td>
			</tr>
<%
purchase_total_amount_1 += asset['purchase1'];
depr_total_amount_1 += asset['depr1'];
left_total_amount_1 += asset['left1'];
purchase_total_amount_2 += asset['purchase_total1'];
depr_total_amount_2 += asset['depr_total1'];
left_total_amount_2 += asset['left_total1'];
purchase_total_amount_3 += asset['purchase_total2'];
depr_total_amount_3 += asset['depr_total2'];
left_total_amount_3 += asset['left_total2'];
%>
			%endfor

			<tr>
				<td style="border-top:2px solid"></td>
				<td style="border-top:2px solid;text-align:right"><b>${_("Kopā par atskaiti:")}</b></td>
				<td style="border-top:2px solid"><b>${_("Perioda sākumā:")}</b></td>
				<td style="border-top:2px solid;text-align:right"><b>${"%0.2f" % (purchase_total_amount_1)}</b></td>
				<td style="border-top:2px solid;text-align:right"><b>${"%0.2f" % (depr_total_amount_1)}</b></td>
				<td style="border-top:2px solid;text-align:right"><b>${"%0.2f" % (left_total_amount_1)}</b></td>
			</tr>
			<tr>
				<td colspan="2" style="border-style:none"></td>
				<td style="border-style:none"><b>${_("Izmaiņa:")}</b></td>
				<td style="border-style:none;text-align:right"><b>${"%0.2f" % (purchase_total_amount_2)}</b></td>
				<td style="border-style:none;text-align:right"><b>${"%0.2f" % (depr_total_amount_2)}</b></td>
				<td style="border-style:none;text-align:right"><b>${"%0.2f" % (left_total_amount_2)}</b></td>
			</tr>
			<tr>
				<td colspan="2" style="border-style:none"></td>
				<td style="border-style:none"><b>${_("Perioda beigās:")}</b></td>
				<td style="border-style:none;text-align:right"><b>${"%0.2f" % (purchase_total_amount_3)}</b></td>
				<td style="border-style:none;text-align:right"><b>${"%0.2f" % (depr_total_amount_3)}</b></td>
				<td style="border-style:none;text-align:right"><b>${"%0.2f" % (left_total_amount_3)}</b></td>
			</tr>
		</tbody>
	</table>
</body>
</html>
