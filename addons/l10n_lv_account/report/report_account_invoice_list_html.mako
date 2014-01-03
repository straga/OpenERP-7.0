<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <% setLang(user.lang) %>
    <span class="title">${reduce(lambda x, obj: (obj.type in ['out_invoice'] and _("List of Invoices")) or (obj.type in ['in_invoice'] and _("List of Supplier Invoices")) or (obj.type in ['out_refund'] and _("List of Refunds")) or (obj.type in ['in_refund'] and _("List of Supplier Refunds")) or '', lines(data['form']), 0)}</span>
    <br/>
	<br/>
    <table class="list_table"  width="100%">
        <thead>
			<tr>
				<th class>${_("Invoice Date")}</th>
				<th class>${_("Number")}</th>
				<th class>${_("Internal Number")}</th>
				<th class>${reduce(lambda x, obj: (obj.type in ['out_invoice', 'out_refund'] and _("Customer")) or (obj.type in ['in_invoice', 'in_refund'] and _("Supplier")) or '', lines(data['form']), 0)}</th>
				<th class>${_("Amount Total")}</th>
				<th class>${_("Amount Untaxed")}</th>
				<th class>${_("Tax")}</th>
				<th class>${_("Due Date")}</th>
			</tr>
		</thead>
        <tbody>
<%
	curr_curr = None;
%>
<%
	amount_total = 0.0;
	amount_untaxed = 0.0;
	amount_tax = 0.0;
%>
			%for inv in lines(data['form']) :
				%if curr_curr != inv.currency_id and curr_curr != None :
        	<tr>
				<td style="border-style:none"/>
				<td style="border-style:none"/>
				<td style="border-style:none"/>
				<td style="border-top:2px solid">
					<b>Total:</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${amount_total}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${amount_untaxed}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${amount_tax}</b>
				</td>
				<td style="border-style:none"/>
			</tr>
				%endif
				%if curr_curr != inv.currency_id :
			<tr>
				<td style="border-top:none;text-align:left"><b>${inv.currency_id.name}</b></td>
			</tr>
				<%
				amount_total = 0.0;
				amount_untaxed = 0.0;
				amount_tax = 0.0;
%>
				<%
				curr_curr = inv.currency_id
%>
				%endif
        	<tr>
				<td><div class="nobreak">${inv.date_invoice or ''}</div></td>
				<td><div class="nobreak">${inv.number or ''}</div></td>
				<td style="text-align:center;"><div class="nobreak">${inv.move_id.internal_sequence_number or ''}</div></td>
				<td style="text-align:left;"><div class="nobreak">${inv.partner_id.name or ''}</div></td>
				<td style="text-align:right;"><div class="nobreak">${inv.amount_total or ''}</div></td>
				<td style="text-align:right;"><div class="nobreak">${inv.amount_untaxed or ''}</div></td>
				<td style="text-align:right;"><div class="nobreak">${inv.amount_tax or ''}</div></td>
				<td style="text-align:right;"><div class="nobreak">${inv.date_due or ''}</div></td>
			</tr>
				%if curr_curr == inv.currency_id :
				<%
				amount_total += inv.amount_total
				amount_untaxed += inv.amount_untaxed
				amount_tax += inv.amount_tax
				%>
				%endif
			%endfor
        	<tr>
				<td style="border-style:none"/>
				<td style="border-style:none"/>
				<td style="border-style:none"/>
				<td style="border-top:2px solid">
					<b>Total:</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${amount_total}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${amount_untaxed}</b>
				</td>
				<td style="border-top:2px solid;text-align:right">
					<b>${amount_tax}</b>
				</td>
				<td style="border-style:none"/>
			</tr>
        </tbody>
    </table>
</body>
</html>
