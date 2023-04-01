from odoo import models
class VisaXlsx(models.AbstractModel):
    _name = 'report.details.visa_xls'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, quotations):
        print(data)
        print(quotations)
        report_name = 'quotations'
        sheet = workbook.add_worksheet(report_name[:31])
        bold = workbook.add_format({'bold': True,'align': 'center',})
        center = workbook.add_format({ 'align': 'center', })
        bold.set_align('vcenter')
        header = workbook.add_format({'bold': True,'align': 'center', 'bg_color': 'blue','color':'white'})
        leftheader = workbook.add_format({'bold': True,'align': 'center', 'bg_color': '#ebe1e4'})
        leftheader.set_align('vcenter')
        sheet.write(0, 0, 'ID', header)
        sheet.write(0, 2, 'ID', header)
        sheet.write(0, 1, 'serial', header)
        sheet.write(0, 3, 'Passenger', header)
        sheet.write(0, 4, 'Age type', header)
        sheet.write(0, 5, 'relationship', header)
        sheet.write(0, 6, 'visa type', header)
        sheet.write(0, 7, 'visa situation', header)
        sheet.write(0, 8, 'receiving date', header)
        sheet.write(0, 9, 'cost', header)
        i=1
        counter=1
        users_count=1

        visa_embassy_client=0
        visa_embassy_company=0
        visa_embassy_assist_only=0
        visa_online_client=0
        visa_online_company=0
        visa_no_visa_required=0

        visa_paper_required_from_client=0
        visa_received_visa_documents=0
        visa_submitted_to_embassy=0
        visa_rejected=0
        visa_online_visa_passport_delivered=0
        visa_received_online_visa=0
        visa_sent_online_visa_to_client=0



        for obj in quotations:
            # One sheet by partner


            visa=list(obj.sale_order_visa)



            if len(visa)==1:
                sheet.write(i, 0,  counter, bold)
                counter += 1
            elif len(visa)>1:
                sheet.merge_range(i, 0, i + len(visa) - 1, 0, counter, bold)
                counter+=1
            for iterator in range(len(visa)):
                print(len(obj.sale_order_flight_int.filtered(lambda item:item.flight_status=='hold')))
                sheet.write(i, 2, users_count, center)
                users_count += 1
                sheet.write(i, 1, obj.name)
                sheet.write(i, 3, visa[iterator].name if visa[iterator].name else '' )
                sheet.write(i, 4, visa[iterator].age_on_travel_date if visa[iterator].age_on_travel_date else '' )
                sheet.write(i, 5, visa[iterator].visa_type if visa[iterator].visa_type else '')
                sheet.write(i, 6, visa[iterator].visa_situation if visa[iterator].visa_situation else '')
                sheet.write(i, 7, f'{visa[iterator].embassy_appointment}' if visa[iterator].embassy_appointment else '')
                sheet.write(i, 8, visa[iterator].receiving_date if visa[iterator].receiving_date else '')
                sheet.write(i, 9, visa[iterator].cost if visa[iterator].cost else '')

                i+=1
                # print(self.env['sale.order.vaccination']._fields['vaccine_type'].selection).get(vaccine[iterator].vaccine_type)

            visa_embassy_client += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_type == 'embassy_client'))
            visa_embassy_company += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_type == 'embassy_company'))
            visa_embassy_assist_only += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_type == 'embassy_assist_only'))
            visa_online_client += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_type == 'online_client'))
            visa_online_company += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_type == 'online_company'))
            visa_no_visa_required+= len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_type == 'no_visa_required'))

            visa_paper_required_from_client+= len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_situation == 'paper_required_from_client'))
            visa_received_visa_documents+= len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_situation == 'received_visa_documents'))
            visa_submitted_to_embassy+= len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_situation == 'submitted_to_embassy'))
            visa_rejected += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_situation == 'rejected'))
            visa_online_visa_passport_delivered += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_situation == 'online_visa_passport_delivered'))
            visa_received_online_visa += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_situation == 'received_online_visa'))
            visa_sent_online_visa_to_client += len(obj.sale_order_visa_inv.filtered(lambda item: item.visa_situation == 'sent_online_visa_to_client'))



        i += 2
        sheet.write(i, 1, 'visa type', header)
        sheet.write(i, 2, 'total', header)
        i+=1
        sheet.merge_range(i, 0, i + 5, 0, 'Visa', leftheader)
        sheet.write(i, 1, 'embassy_client')
        sheet.write(i, 2, visa_embassy_client, bold)
        i += 1
        sheet.write(i, 1, 'embassy_company')
        sheet.write(i, 2, visa_embassy_company, bold)
        i += 1
        sheet.write(i, 1, 'embassy_assist_only')
        sheet.write(i, 2, visa_embassy_assist_only, bold)
        i += 1
        sheet.write(i, 1, 'online_client')
        sheet.write(i, 2, visa_online_client, bold)
        i += 1
        sheet.write(i, 1, 'online_company')
        sheet.write(i, 2, visa_online_company, bold)
        i += 1
        sheet.write(i, 1, 'no_visa_required')
        sheet.write(i, 2, visa_no_visa_required, bold)
        i += 2

        sheet.write(i, 1, 'visa situation', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 6, 0, 'Visa', leftheader)
        sheet.write(i, 1, 'paper_required_from_client')
        sheet.write(i, 2, visa_paper_required_from_client, bold)
        i += 1
        sheet.write(i, 1, 'received_visa_documents')
        sheet.write(i, 2, visa_received_visa_documents, bold)
        i += 1
        sheet.write(i, 1, 'submitted_to_embassy')
        sheet.write(i, 2, visa_submitted_to_embassy, bold)
        i += 1
        sheet.write(i, 1, 'rejected')
        sheet.write(i, 2, visa_rejected, bold)
        i += 1
        sheet.write(i, 1, 'online_visa_passport_delivered')
        sheet.write(i, 2, visa_online_visa_passport_delivered, bold)
        i += 1
        sheet.write(i, 1, 'received_online_visa')
        sheet.write(i, 2, visa_received_online_visa, bold)
        i += 1
        sheet.write(i, 1, 'sent_online_visa_to_client')
        sheet.write(i, 2, visa_sent_online_visa_to_client, bold)
