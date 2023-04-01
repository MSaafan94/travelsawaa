from odoo import models
class ProgramXlsx(models.AbstractModel):
    _name = 'report.details.program_xls'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, quotations):
        print(data)
        print(quotations)
        report_name = 'Program'
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
        sheet.write(0, 3, 'BUS', header)
        sheet.write(0, 4, 'Passenger', header)
        sheet.write(0, 5, 'Age type', header)
        sheet.write(0, 6, 'program status', header)
        sheet.write(0, 7, 'program name', header)
        sheet.write(0, 8, 'program Description', header)

        i=1
        counter=1
        users_count=1

        child_take_program=0
        child_not_take_program=0
        adult_take_program=0
        adult_not_take_program=0


        for obj in quotations:
            # One sheet by partner

            program=list(obj.sale_order_program)


            if len(program)==1:
                sheet.write(i, 0,  counter, bold)
                counter += 1
            elif len(program)>1:
                sheet.merge_range(i, 0, i + len(program) - 1, 0, counter, bold)
                counter+=1
            for iterator in range(len(program)):
                sheet.write(i, 2, users_count, center)
                users_count += 1
                sheet.write(i, 1, obj.name)
                sheet.write(i, 3, '')
                sheet.write(i, 4, program[iterator].name if program[iterator].name else '')
                sheet.write(i, 5, program[iterator].age_type if program[iterator].age_type else '')

                sheet.write(i, 6, program[iterator].status if program[iterator].status else '')
                names=''
                for name in program[iterator].program_name:
                    print(name)
                    names+= name.name+' ,' if name else ''
                sheet.write(i, 7, names)
                sheet.write(i, 8, program[iterator].description if program[iterator].description else '')

                i+=1
                # print(self.env['sale.order.vaccination']._fields['vaccine_type'].selection).get(vaccine[iterator].vaccine_type)

            child_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'child' and item.program_name))
            adult_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'adult' and item.program_name))
            child_not_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'child' and not item.program_name))
            adult_not_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'adult' and not item.program_name))


        i += 2

        sheet.write(i, 1, 'program', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 3, 0, 'program', leftheader)
        sheet.write(i, 1, 'adult take program')
        sheet.write(i, 2, adult_take_program, bold)
        i += 1
        sheet.write(i, 1, 'adult not take program')
        sheet.write(i, 2, adult_not_take_program, bold)
        i+=1
        sheet.write(i, 1, 'child take program')
        sheet.write(i, 2, child_take_program, bold)
        i += 1
        sheet.write(i, 1, 'child not take program')
        sheet.write(i, 2, child_not_take_program, bold)

        i += 2






