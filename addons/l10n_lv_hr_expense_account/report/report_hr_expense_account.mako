<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <% setLang(user.lang) %>
	%for exp in lines(data['form']) :
    <span>${_("Name Surname:")} ${exp.employee_id.name}</span><br/>
    <span>${_("Identification No:")} ${exp.employee_id.identification_id or ''}</span><br/>
    <span>${_("Department:")} ${exp.employee_id.department_id.name or ''}</span><br/>
    <span>${_("Bank Account:")} ${exp.employee_id.bank_account_id.acc_number or ''}</span><br/>
    <span>${_("Currency:")} ${exp.employee_id.company_id.currency_id.name or ''}</span><br/>
    <br/>
    <span class="title"><center>${_("EXPENSE No")} ${exp.name}</center></span><br/>
    <span><center>${data['form']['date_from']} - ${data['form']['date_to']}</center></span><br/>
    <br/>
    <br/>
    <span>${_("Received:")}</span><br/>
    <table class="list_table" width="100%">
        <tr>
			<th class width="10%">${_("Doc. No")}</th>
			<th class width="15%">${_("Journal Entry No")}</th>
			<th class width="10%">${_("Doc. Date")}</th>
			<th class width="40%">${_("Justification")}</th>
			<th class width="10%">${_("Account")}</th>
			<th class width="15%">${_("Amount")}</th>
        </tr>
<%
total_received = 0.0
total_spent = 0.0
%>
        %for bank_line in bank_lines(data['form']) :
            %for move in bank_line.move_ids:
                %for move_line in move.line_id:
                    %if move_line.account_id.id == exp.employee_id.address_home_id.property_account_receivable.id :
        <tr>
            <td>${move_line.invoice_code or ''}</td>
            <td style="text-align: center;">${move_line.move_id.internal_sequence_number or ''}</td>
            <td style="text-align: center;">${move_line.date}</td>
            <td>${move_line.name}</td>
            <td style="text-align: center;">${move_line.account_id.code}</td>
            <td style="text-align: right;">${move_line.credit}</td>
        </tr>
                    <%
                    total_received += move_line.credit
                    %>
                    %endif
                %endfor
            %endfor
        %endfor
        <tr>
            <td style="border-style:none"/>
            <td style="border-style:none"/>
            <td style="border-style:none"/>
            <td style="border-style:none"/>
            <td style="border-top:2px solid"><b>${_("Total:")}</b></td>
            <td style="border-top:2px solid;text-align:right"><b>${total_received}</b></td>
        </tr>
    </table><br/>
    <br/>
    <span>${_("Spent:")}</span><br/>
    <table class="list_table" width="100%">
	    <tr>
			<th class width="10%">${_("Doc. No")}</th>
			<th class width="15%">${_("Journal Entry No")}</th>
			<th class width="10%">${_("Doc. Date")}</th>
			<th class width="40%">${_("Justification")}</th>
			<th class width="10%">${_("Account")}</th>
			<th class width="15%">${_("Amount")}</th>
        </tr>
        %for line in exp.account_move_id.line_id:
            %if line.tax_code_id:
<%
partner_name = line.partner_id and (line.partner_id.name + ', ') or ''
partner_vat = (line.partner_id and line.partner_id.vat) and (_("TIN ") + line.partner_id.vat + ', ') or ''
%>
        <tr>
            <td>${line.invoice_code or ''}</td>
            <td style="text-align: center;">${line.move_id.internal_sequence_number or ''}</td>
            <td style="text-align: center;">${line.date}</td>
            <td>${partner_name}${partner_vat}${line.name}</td>
            <td style="text-align: center;">${line.account_id.code}</td>
            <td style="text-align: right;">${line.debit}</td>
        </tr>
            <%
            total_spent += line.debit
            %>
            %endif
        %endfor
        <tr>
            <td style="border-style:none"/>
            <td style="border-style:none"/>
            <td style="border-style:none"/>
            <td style="border-style:none"/>
            <td style="border-top:2px solid"><b>${_("Total:")}</b></td>
            <td style="border-top:2px solid;text-align:right"><b>${total_spent}</b></td>
        </tr>
    </table><br/>
    <br/>
    <table width="100%">
        <tr>
            <td width="50%"></td>
            <td width="50%">${_("Expense Person:")}</td>
        </tr>
        <tr>
            <td width="50%"></td>
            <td width="50%">${_("Accountant:")}</td>
        </tr>
        <tr>
            <td width="50%"></td>
            <td width="50%">${_("Manager:")}</td>
        </tr>
    </table>
    %endfor
</body>
</html>
