from odoo import models
class AccomodationXlsx(models.AbstractModel):
    _name = 'report.details.accomodation_xls'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, quotations):
        print(data)
        print(quotations)
        report_name = 'accomodation'
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
        sheet.write(0, 5, 'Age', header)
        sheet.write(0, 6, 'Age type', header)
        sheet.write(0, 7, 'relationship', header)
        sheet.write(0, 8, 'Whatsapp', header)
        sheet.write(0, 9, 'mobile', header)
        sheet.write(0, 10, 'Hotel', header)
        sheet.write(0, 11, 'Check in', header)
        sheet.write(0, 12, 'Check out', header)
        sheet.write(0, 13, 'Nights', header)
        sheet.write(0, 14, 'Room id', header)
        sheet.write(0, 15, 'Room type', header)
        sheet.write(0, 16, 'Room view', header)
        sheet.write(0, 17, 'Meal plan', header)
        sheet.write(0, 18, 'notes', header)

        i=1
        counter=1
        users_count = 1

        for obj in quotations:
            # One sheet by partner


            accomodation=list(obj.sale_order_accommodation)


            if len(accomodation)==1:
                sheet.write(i, 0,  counter, bold)
                counter+=1
            elif len(accomodation)>1:
                sheet.merge_range(i, 0, i + len(accomodation) - 1, 0, counter, bold)
                counter+=1
            for iterator in range(len(accomodation)):
                print(len(obj.sale_order_flight_int.filtered(lambda item:item.flight_status=='hold')))
                sheet.write(i, 2, users_count, center)
                users_count += 1
                sheet.write(i, 1, obj.name)
                sheet.write(i, 3, '')
                sheet.write(i, 4, accomodation[iterator].name if accomodation[iterator].name else '' )
                sheet.write(i, 5, accomodation[iterator].age_on_travel_date if accomodation[iterator].age_on_travel_date else '' )
                sheet.write(i, 6, accomodation[iterator].age_type if accomodation[iterator].age_type else '')
                sheet.write(i, 7, accomodation[iterator].relation if accomodation[iterator].relation else '')
                sheet.write(i, 8, accomodation[iterator].whatsapp_num if accomodation[iterator].whatsapp_num else '')
                sheet.write(i, 9, accomodation[iterator].phone_number if accomodation[iterator].phone_number else '')
                hotel = ''
                for hotelobj in accomodation[iterator].hotel_name:
                    hotel += hotelobj.hotel + ' ,' if hotelobj.hotel else ''
                sheet.write(i, 10, hotel)
                sheet.write(i, 11, f'{accomodation[iterator].check_in_date}' if accomodation[iterator].check_in_date else '')
                sheet.write(i, 12, f'{accomodation[iterator].check_out_date}' if accomodation[iterator].check_out_date else '')
                sheet.write(i, 13, accomodation[iterator].no_of_nights if accomodation[iterator].no_of_nights else '')
                sheet.write(i, 14, accomodation[iterator].room_id if accomodation[iterator].room_id else '')
                sheet.write(i, 15, accomodation[iterator].room_type if accomodation[iterator].room_type else '')
                sheet.write(i, 16, accomodation[iterator].room_view.name if accomodation[iterator].room_view.name else '')
                sheet.write(i, 17, accomodation[iterator].meal_plan.name if accomodation[iterator].meal_plan.name else '')
                sheet.write(i, 18, accomodation[iterator].notes if accomodation[iterator].notes else '')
                i+=1
                # print(self.env['sale.order.vaccination']._fields['vaccine_type'].selection).get(vaccine[iterator].vaccine_type)

