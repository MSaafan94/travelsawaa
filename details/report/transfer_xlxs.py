from odoo import models
class TreansferXlsx(models.AbstractModel):
    _name = 'report.details.transfer_xls'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, quotations):
        print(data)
        print(quotations)
        report_name = 'transfer'
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
        sheet.write(0, 4, 'Vehicle Type', header)
        sheet.write(0, 5, 'Date Of Transfer', header)
        sheet.write(0, 6, 'Pick Up Time', header)
        sheet.write(0, 7, 'route', header)
        sheet.write(0, 8, 'Transfer cost', header)

        i=1
        counter=1
        users_count=1

        for obj in quotations:
            # One sheet by partner

            transfer=list(obj.sale_order_transfer)


            if len(transfer)==1:
                sheet.write(i, 0,  counter, bold)
                counter += 1
            elif len(transfer)>1:
                sheet.merge_range(i, 0, i + len(transfer) - 1, 0, counter, bold)
                counter+=1
            for iterator in range(len(transfer)):
                sheet.write(i, 2, users_count, center)
                users_count += 1
                sheet.write(i, 1, obj.name)
                sheet.write(i, 3, transfer[iterator].name if transfer[iterator].name else '')
                sheet.write(i, 4, transfer[iterator].vehicle_type.name if transfer[iterator].vehicle_type.name else '')

                sheet.write(i, 5, f'{transfer[iterator].date_of_transfer}' if transfer[iterator].date_of_transfer else '')
                sheet.write(i, 6, transfer[iterator].pick_up_time if transfer[iterator].pick_up_time else '')
                sheet.write(i, 7, transfer[iterator].route if transfer[iterator].route else '')
                sheet.write(i, 8, transfer[iterator].transfer_cost if transfer[iterator].transfer_cost else '')

                i+=1
                # print(self.env['sale.order.vaccination']._fields['vaccine_type'].selection).get(vaccine[iterator].vaccine_type)

