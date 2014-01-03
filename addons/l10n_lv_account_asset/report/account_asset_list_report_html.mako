<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <% setLang(user.lang) %>
	<span class="title">${_("Pamatlīdzekļu saraksts ")}</span>
	<span>${_("uz ")}${data['form']['date']}</span>
	<br/>
	<br/>
    <table class="list_table"  width="100%">
        <thead>
			<tr>
				<th colspan="3" class></th>
				<th class>${_("Uzskaites vērtība")}</th>
				<th class>${_("Nolietojums")}</th>
				<th class>${_("Atlikusī vērtība")}</th>
			</tr>
		</thead>
<%
	curr_acc = None;
%>
<%
	account_total_purchase = 0.0;
	account_total_depr = 0.0;
	account_total_left = 0.0;
	total_purchase = 0.0;
	total_depr = 0.0;
	total_left = 0.0;
	count = 1;
%>
		<tbody>
			%for asset in lines(data['form']) :
				%if curr_acc != asset.category_id.account_asset_id and curr_acc != None :
        	<tr>
				<td>
					<b>Kopā kontā:</b>
				</td>
				<td colspan="2"></td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (account_total_purchase)}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (account_total_depr)}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (account_total_left)}</b>
				</td>
			</tr>
				%endif
				%if curr_acc != asset.category_id.account_asset_id :
			<tr>
				<td style="border-top:none;text-align:left"><b>${_("Konts:")}</b></td>
				<td style="border-top:none;text-align:left"><b>${asset.category_id.account_asset_id.code}</b></td>
				<td style="border-top:none;text-align:left"><b>${asset.category_id.account_asset_id.name}</b></td>
				<td colspan="3"/>
			</tr>
				<%
				account_total_purchase = 0.0;
				account_total_depr = 0.0;
				account_total_left = 0.0;
				count = 1;
%>
				<%
				curr_acc = asset.category_id.account_asset_id
%>
				%endif
			<tr>
				<td>${count}</td>
				<td colspan="2">${asset.name}</td>
				<td style="text-align:right">${"%0.2f" % (asset.purchase_value)}</td>
<%
depr = 0.0
%>
				%for line in asset.depreciation_line_ids:
					%if line.move_check == True and line.depreciation_date <= data['form']['date']:
						<%
						depr += line.amount
						%>
					%endif
				%endfor
				<td style="text-align:right">${"%0.2f" % (depr)}</td>
<%
left = asset.purchase_value - depr
%>
				<td style="text-align:right">${"%0.2f" % (left)}</td>
			</tr>
				%if curr_acc == asset.category_id.account_asset_id :
				<%
				account_total_purchase += asset.purchase_value
				account_total_depr += depr
				account_total_left += left
				count += 1
				%>
				%endif
<%
total_purchase += asset.purchase_value
total_depr += depr
total_left += left
%>
			%endfor
        	<tr>
				<td colspan="3">
					<b>Kopā kontā:</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (account_total_purchase)}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (account_total_depr)}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (account_total_left)}</b>
				</td>
			</tr>
        	<tr>
				<td colspan="3" style="border-top:2px solid">
					<b>Kopā pavisam:</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (total_purchase)}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (total_depr)}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${"%0.2f" % (total_left)}</b>
				</td>
			</tr>
		</tbody>
	</table>
</body>
</html>
