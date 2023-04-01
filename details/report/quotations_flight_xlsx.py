from odoo import models
class flightXlsx(models.AbstractModel):
    _name = 'report.details.quotationflight_xls'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, quotations):
        report_name = 'flight'
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
        sheet.write(0, 4, 'flight status ', header)
        sheet.write(0, 5, 'flight type ', header)
        sheet.write(0, 6, 'extra luggage ', header)
        sheet.write(0, 7, 'flight route', header)
        i=1
        counter=1
        int_grp = 0
        int_sys = 0
        int_without = 0
        int_hold=0
        int_issued=0
        int_waiting_issued=0
        int_sent=0
        int_extra_bag_apr_dep = 0
        int_extra_bag_on_arr=0
        int_extra_bag_on_dep=0
        int_arp_and_dep=0
        int_departure_only=0
        int_arrival_only=0

        users_count=1



        for obj in quotations:
            # One sheet by partner


            flight_int=list(obj.sale_order_flight_int)


            if len(flight_int)==1:
                sheet.write(i, 0,  counter, bold)
            elif len(flight_int)>1:
                sheet.merge_range(i, 0, i + len(flight_int) - 1, 0, counter, bold)
                counter+=1
            for iterator in range(len(flight_int)):
                print(len(obj.sale_order_flight_int.filtered(lambda item:item.flight_status=='hold')))
                sheet.write(i, 2, users_count, center)
                users_count += 1
                sheet.write(i, 1, obj.name)
                sheet.write(i, 3, flight_int[iterator].name if flight_int[iterator].name else '')
                sheet.write(i, 4, flight_int[iterator].flight_status if flight_int[iterator].flight_status else '')
                sheet.write(i, 5, flight_int[iterator].flight_type if flight_int[iterator].flight_type else '')
                sheet.write(i, 6, flight_int[iterator].extra_luggage if flight_int[iterator].extra_luggage else '')
                sheet.write(i, 7, flight_int[iterator].route if flight_int[iterator].extra_luggage else '')

                i+=1
                # print(self.env['sale.order.vaccination']._fields['vaccine_type'].selection).get(vaccine[iterator].vaccine_type)
            int_grp += len(obj.sale_order_flight_int.filtered(lambda item:item.flight_type=='int_grp'))
            int_sys +=len(obj.sale_order_flight_int.filtered(lambda item:item.flight_type=='int_sys'))
            int_without+=len(obj.sale_order_flight_int.filtered(lambda item:item.flight_type=='without_flight'))
            int_hold+=len(obj.sale_order_flight_int.filtered(lambda item: item.flight_status == 'hold'))
            int_issued+=len(obj.sale_order_flight_int.filtered(lambda item: item.flight_status == 'issued'))
            int_waiting_issued+=len(obj.sale_order_flight_int.filtered(lambda item: item.flight_status == 'waiting_issuing'))
            int_sent+=len(obj.sale_order_flight_int.filtered(lambda item: item.flight_status == 'sent_to_client'))
            int_extra_bag_apr_dep += len(obj.sale_order_flight_int.filtered(lambda item: item.extra_luggage == 'extra_bag_apr_dep'))
            int_extra_bag_on_arr+=len(obj.sale_order_flight_int.filtered(lambda item: item.extra_luggage == 'extra_bag_on_arr'))
            int_extra_bag_on_dep+=len(obj.sale_order_flight_int.filtered(lambda item: item.extra_luggage == 'extra_bag_on_dep'))
            int_arp_and_dep+=len(obj.sale_order_flight_int.filtered(lambda item: item.route == 'APR&DEP'))
            int_departure_only+=len(obj.sale_order_flight_int.filtered(lambda item: item.route == 'departure_only'))
            int_arrival_only+=len(obj.sale_order_flight_int.filtered(lambda item: item.route == 'arrival_only'))


        i+=2
        sheet.write(i, 1, 'flight type', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 2, 0, 'international flight', leftheader)
        sheet.write(i,1 , 'International group')
        sheet.write(i, 2, int_grp, bold)
        i+=1
        sheet.write(i, 1, 'International system')
        sheet.write(i, 2, int_sys, bold)
        i+=1
        sheet.write(i, 1, 'Without flight')
        sheet.write(i, 2, int_without, bold)



        i += 2
        sheet.write(i, 1, 'flight status', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 3, 0, 'international flight', leftheader)
        sheet.write(i, 1, 'hold')
        sheet.write(i, 2, int_hold, bold)
        i+=1
        sheet.write(i, 1, 'Issued')
        sheet.write(i, 2, int_issued, bold)
        i+=1
        sheet.write(i, 1, 'Waiting Issuing ')
        sheet.write(i, 2, int_waiting_issued, bold)
        i+=1
        sheet.write(i, 1, 'Sent to Client ')
        sheet.write(i, 2, int_sent,bold)




        i += 2
        sheet.write(i, 1, 'Extra luggaga', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 2, 0, 'international flight', leftheader)
        sheet.write(i, 1, 'Extra Bag Apr and DEP')
        sheet.write(i, 2, int_extra_bag_apr_dep, bold)
        i+=1
        sheet.write(i, 1, 'Extra Bag on ARR')
        sheet.write(i, 2, int_extra_bag_on_arr, bold)
        i+=1
        sheet.write(i, 1, 'Extra Bag on DEP')
        sheet.write(i, 2,int_extra_bag_on_dep ,bold)



        i += 2
        sheet.write(i, 1, 'flight route', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 2, 0, 'international flight', leftheader)
        sheet.write(i, 1, 'APR and DEP')
        sheet.write(i, 2, int_arp_and_dep, bold)
        i+=1
        sheet.write(i, 1, 'departure only')
        sheet.write(i, 2, int_departure_only, bold)
        i+=1
        sheet.write(i, 1, 'Arrival only')
        sheet.write(i, 2, int_arrival_only, bold)

