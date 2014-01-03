<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<style type="text/css">
        ${css}
      img.logo {
      width: auto;
      height: 2cm;
      }
    </style>
</head>

<body>
	%for inv in objects :
	<% setLang(inv.partner_id.lang) %>
	%if inv.company_id.logo:
            <div style="position:absolute;top:0;left:0;">
		<img src='${"data:image/gif;base64," + inv.company_id.logo}' class='logo'></img>
	    </div>
	%endif
	<div style="position:absolute;top:3cm;left:0;">
	    <table class="basic_table" width="100%">
		<tr>
		    <td style="font-size:14 !important;text-align:left;"><b>${inv.partner_id.name}</b></td>
		    <td style="font-size:14 !important;text-align:right;"><b>Rēķins Nr. ${inv.number}</b></td>
		</tr>
<%
address_inv = inv.address_invoice_id
if address_inv:
    street_inv = address_inv.street
    city_inv = address_inv.city
    zip_inv = address_inv.zip
    state_inv = address_inv.state_id and address_inv.state_id.name or ''
    country_inv = address_inv.country_id and address_inv.country_id.name or ''
    address_inv_disp = (street_inv and street_inv or '') + ((street_inv and (city_inv or zip_inv or state_inv or country_inv)) and ', ' or '') + (city_inv and city_inv or '') + ((city_inv and (zip_inv or state_inv or country_inv)) and ', ' or '') + (zip_inv and zip_inv or '') + ((zip_inv and (state_inv or country_inv)) and ', ' or '') + (state_inv and state_inv or '') + ((zip_inv and country_inv) and ', ' or '') + (country_inv and country_inv or '')
%>
		<tr>
		    <td>${address_inv and address_inv_disp or ''}</td>
		    <td style="text-align:right;">${inv.date_invoice}</td>
		</tr>
	    </table>
	</div>

	<div style="position:absolute;top:5cm;left:0;">
	<table class="basic_table" width="100%">
	    <tr>
		<td width='16%' style="font-size:11 !important;"><font color='#585858'>Saņēmēja rekvizīti:</font></td>
		<td width='84%'></td>
	    </tr>
	    <tr>
		<td width='16%' style="font-size:11 !important;"><font color='#585858'>Nosaukums:</font></td>
		<td width='84%'><b>${inv.partner_id.name}</b></td>
	    </tr>
	    <tr>
		<td width='16%' style="font-size:11 !important;"><font color='#585858'>PVN reģistrācijas Nr.:</font></td>
		<td width='84%'>${inv.partner_id.vat or ''}</td>
	    </tr>
<%
address = inv.partner_id.address_id
if address:
    street = address[0].street
    city = address[0].city
    zip = address[0].zip
    state = address[0].state_id and address[0].state_id.name or ''
    country = address[0].country_id and address[0].country_id.name or ''
    address_disp = (street and street or '') + ((street and (city or zip or state or country)) and ', ' or '') + (city and city or '') + ((city and (zip or state or country)) and ', ' or '') + (zip and zip or '') + ((zip and (state or country)) and ', ' or '') + (state and state or '') + ((zip and country) and ', ' or '') + (country and country or '')
%>
	    <tr>
		<td width='16%' style="font-size:11 !important;"><font color='#585858'>Adrese:</font></td>
		<td width='84%'>${address and address_disp or ''}</td>
	    </tr>
	    <tr>
		<td width='16%' style="font-size:11 !important;"><font color='#585858'>Norēķinu konts:</font></td>
		%if inv.partner_id.bank_ids:
		%for b in inv.partner_id.bank_ids:
		<td width='84%'>${b.acc_number}, ${b.bank_name}</td>
	    </tr>
	    <tr>
		<td width='16%'></td>
		%endfor
		%endif
		<td width='84%'></td>
	    </tr>
	    <tr>
		<td width='16%'>&nbsp;</td>
		<td width='84%'>&nbsp;</td>
	    </tr>
	    <tr>
		<td width='16%' style="font-size:11 !important;"><font color='#585858'>Apmaksas termiņš:</font></td>
		<td width='84%'>${inv.date_due or inv.date_invoice or ''}</td>
	    </tr>
	</table>
	<br/>
	<table class="list_table" width="100%">
	    <thead>
		<tr style="border-top:1px solid;background-color:#F8F8F8;color:#585858;">
		    <th style="border-bottom:1px solid !important;font-weight:normal !important;">Nr.</th>
		    <th class="description" width="45%" style="border-bottom:1px solid !important;font-weight:normal !important;">Nosaukums</th>
		    <th style="border-bottom:1px solid !important;font-weight:normal !important;">Mērv.</th>
		    <th style="border-bottom:1px solid !important;font-weight:normal !important;">Daudzums</th>
		    <th style="border-bottom:1px solid !important;font-weight:normal !important;">Cena, ${inv.currency_id.name}</th>
		    <th style="border-bottom:1px solid !important;font-weight:normal !important;">Summa, ${inv.currency_id.name}</th>
		</tr>
	    </thead>
	    <tbody>
<%
seq = 0
%>
	    %for line in inv.invoice_line :
<%
seq += 1
%>
		<tr>
		    <td style="font-size:12 !important;">${seq}.</td>
		    <td class="description" style="font-size:12 !important;">${line.name}</td>
		    <td style="font-size:12 !important;">${line.uos_id.name or ''}</td>
		    <td style="font-size:12 !important;">${line.quantity}</td>
		    <td style="font-size:12 !important;">${formatLang(line.price_unit)}</td>
		    <td style="font-size:12 !important;">${formatLang(line.price_subtotal)}</td>
		</tr>
	    %endfor
		<tr>
		    <td colspan="2" style="text-align:left;border-top:1px solid;font-size:12 !important;">Kopā:</td>
		    <td colspan="3" style="border-top:1px solid;font-size:12 !important;"></td>
		    <td class="numbers" style="border-top:1px solid;font-size:12 !important;">${formatLang(inv.amount_untaxed)}</td>
		</tr>
	    %if inv.tax_line:
		%for tax in inv.tax_line:
		<tr>
		    <td colspan="2" style="text-align:left;border-style:none;font-size:12 !important;">${tax.name}</td>
		    <td colspan="3" style="border-style:none;font-size:12 !important;"></td>
		    <td class="numbers" style="border-style:none;font-size:12 !important;">${formatLang(tax.amount)}</td>
		</tr>
		%endfor
	    %endif
	    %if not inv.tax_line:
		<tr>
		    <td colspan="2" style="text-align:left;border-style:none;font-size:12 !important;">Nodokļi:</td>
		    <td colspan="3" style="border-style:none;font-size:12 !important;"></td>
		    <td class="numbers" style="border-style:none;font-size:12 !important;">${formatLang(inv.amount_tax)}</td>
		</tr>
	    %endif
		<tr>
		    <td colspan="2" style="text-align:left;border-style:none;font-size:14 !important;"><b>Rēķina summa:</b></td>
		    <td colspan="3" style="border-style:none;font-size:12 !important;"></td>
		    <td class="numbers" style="border-style:none;font-size:14 !important;"><b>${formatLang(inv.amount_total)}</b></td>
		</tr>
		<tr>
		    <td colspan="2" style="border-style:none;font-size:12 !important;"></td>
		    <td colspan="4" style="border-style:none;text-align:right;font-size:12 !important;">Summa vārdiem: ${helper.verbose_num_lv(inv.amount_total, inv.currency_id.name)}</td>
		</tr>
	    </tbody>
	</table>
	<br/>
	<table class="basic_table">
	    <tr><td colspan="2" style="font-size:11 !important;"><font color="#585858">Piegādātāja rekvizīti:</font></td></tr>
	    <tr><td><b>${inv.company_id.name}</b></td></tr>
	    <tr><td colspan="2">Vienotais reģistrācijas numurs: <b>${inv.company_id.company_registry or '____________'}</b>, PVN reģistrācijas Nr.: <b>${inv.company_id.vat or '______________'}</b></td></tr>
<%
address_com = inv.company_id.partner_id
if address_com:
    street_com = address_com.street
    city_com = address_com.city
    zip_com = address_com.zip
    state_com = address_com.state_id and address_com.state_id.name or ''
    country_com = address_com.country_id and address_com.country_id.name or ''
    address_com_disp = (street_com and street_com or '') + ((street_com and (city_com or zip_com or state_com or country_com)) and ', ' or '') + (city_com and city_com or '') + ((city_com and (zip_com or state_com or country_com)) and ', ' or '') + (zip_com and zip_com or '') + ((zip_com and (state_com or country_com)) and ', ' or '') + (state_com and state_com or '') + ((zip_com and country_com) and ', ' or '') + (country_com and country_com or '')
%>
	    <tr><td colspan="2">Adrese: ${address_com and address_com_disp or ''}</td></tr>
	    <tr><td style="vertical-align:top;">Norēķinu konts:</td>
	    <td>
	    %if inv.company_id.bank_ids:
		<table class="basic_table">
		%for b in inv.company_id.bank_ids:
		    <tr><td><b>${b.acc_number}</b>, ${b.bank_name}, bankas kods ${b.bank_bic}</td></tr>
		%endfor
		</table>
	    %endif
	    </td></tr>
	    <tr><td colspan="2">&nbsp;</td></tr>
	    <tr><td colspan="2">Apmaksai rēķina summa jāpārskaita uz šajā dokumentā minēto piegādātāja norēķinu kontu.</td></tr>
	    <tr><td colspan="2">Maksājuma mērķī lūdzam norādīt rēķina numuru.</td></tr>
	    <tr><td colspan="2">&nbsp;</td></tr>
	    <tr><td colspan="2">Šis dokuments ir sagatavots elektroniski un ir derīgs bez paraksta.</td></tr>
	</table>
	</div>

	<p style="page-break-after:always"></p>
	
	%endfor
</body>

</html>
