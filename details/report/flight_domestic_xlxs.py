from odoo import models
class flightdomesticXlsx(models.AbstractModel):
    _name = 'report.details.quotationflight_domestic_xls'
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

        dom_grp = 0
        dom_sys = 0
        dom_without = 0
        dom_hold = 0
        dom_issued = 0
        dom_waiting_issued = 0
        dom_sent = 0
        dom_extra_bag_apr_dep = 0
        dom_extra_bag_on_arr = 0
        dom_extra_bag_on_dep = 0
        dom_arp_and_dep = 0
        dom_departure_only = 0
        dom_arrival_only = 0
        users_count=1



        for obj in quotations:
            # One sheet by partner


            flight_dom=list(obj.sale_order_flight_dom)


            if len(flight_dom)==1:
                sheet.write(i, 0,  counter, bold)
            elif len(flight_dom)>1:
                sheet.merge_range(i, 0, i + len(flight_dom) - 1, 0, counter, bold)
                counter+=1
            for iterator in range(len(flight_dom)):
                print(len(obj.sale_order_flight_int.filtered(lambda item:item.flight_status=='hold')))
                sheet.write(i, 2, users_count, center)
                users_count += 1
                sheet.write(i, 1, obj.name)
                sheet.write(i, 3, flight_dom[iterator].name if flight_dom[iterator].name else '')
                sheet.write(i, 4, flight_dom[iterator].flight_status if flight_dom[iterator].flight_status else '')
                sheet.write(i, 5, flight_dom[iterator].flight_type if flight_dom[iterator].flight_type else '')
                sheet.write(i, 6, flight_dom[iterator].extra_luggage if flight_dom[iterator].extra_luggage else '')
                sheet.write(i, 7, flight_dom[iterator].route if flight_dom[iterator].extra_luggage else '')

                i+=1
                # print(self.env['sale.order.vaccination']._fields['vaccine_type'].selection).get(vaccine[iterator].vaccine_type)

            dom_grp += len(obj.sale_order_flight_dom.filtered(lambda item: item.flight_type == 'dom_grp'))
            dom_sys += len(obj.sale_order_flight_dom.filtered(lambda item: item.flight_type == 'dom_sys'))
            dom_without += len(obj.sale_order_flight_dom.filtered(lambda item: item.flight_type == 'without_flight'))
            dom_hold += len(obj.sale_order_flight_dom.filtered(lambda item: item.flight_status == 'hold'))
            dom_issued += len(obj.sale_order_flight_dom.filtered(lambda item: item.flight_status == 'issued'))
            dom_waiting_issued += len(obj.sale_order_flight_dom.filtered(lambda item: item.flight_status == 'waiting_issuing'))
            dom_sent += len(obj.sale_order_flight_dom.filtered(lambda item: item.flight_status == 'sent_to_client'))
            dom_extra_bag_apr_dep += len(obj.sale_order_flight_dom.filtered(lambda item: item.extra_luggage == 'extra_bag_apr_dep'))
            dom_extra_bag_on_arr += len(obj.sale_order_flight_dom.filtered(lambda item: item.extra_luggage == 'extra_bag_on_arr'))
            dom_extra_bag_on_dep += len(obj.sale_order_flight_dom.filtered(lambda item: item.extra_luggage == 'extra_bag_on_dep'))
            dom_arp_and_dep += len(obj.sale_order_flight_dom.filtered(lambda item: item.route == 'APR&DEP'))
            dom_departure_only += len(obj.sale_order_flight_dom.filtered(lambda item: item.route == 'departure_only'))
            dom_arrival_only += len(obj.sale_order_flight_dom.filtered(lambda item: item.route == 'arrival_only'))


        i+=2
        sheet.write(i, 1, 'flight type', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 2, 0, 'domestic flight', leftheader)
        sheet.write(i, 1, 'domestic group')
        sheet.write(i, 2, dom_grp, bold)
        i+=1
        sheet.write(i, 1, 'domestic system')
        sheet.write(i, 2, dom_sys, bold)
        i+=1
        sheet.write(i, 1, 'Without flight')
        sheet.write(i, 2, dom_without, bold)
        i += 2
        sheet.write(i, 1, 'flight status', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 3, 0, 'domestic flight', leftheader)
        sheet.write(i, 1, 'hold')
        sheet.write(i, 2, dom_hold, bold)
        i+=1
        sheet.write(i, 1, 'Issued')
        sheet.write(i, 2, dom_issued, bold)
        i+=1
        sheet.write(i, 1, 'Waiting Issuing ')
        sheet.write(i, 2, dom_waiting_issued, bold)
        i+=1
        sheet.write(i, 1, 'Sent to Client ')
        sheet.write(i, 2, dom_sent, bold)




        i += 2
        sheet.write(i, 1, 'extra luggaga',header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 2, 0, 'domestic flight', leftheader)
        sheet.write(i, 1, 'Extra Bag Apr and DEP')
        sheet.write(i, 2, dom_extra_bag_apr_dep, bold)
        i+=1
        sheet.write(i, 1, 'Extra Bag on ARR')
        sheet.write(i, 2, dom_extra_bag_on_arr, bold)
        i+=1
        sheet.write(i, 1, 'Extra Bag on DEP')
        sheet.write(i, 2, dom_extra_bag_on_dep, bold)



        i += 2
        sheet.write(i, 1, 'flight route',header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 2, 0, 'domestic flight', leftheader)
        sheet.write(i, 1, 'APR and DEP')
        sheet.write(i, 2, dom_arp_and_dep, bold)
        i+=1
        sheet.write(i, 1, 'departure only')
        sheet.write(i, 2, dom_departure_only, bold)
        i+=1
        sheet.write(i, 1, 'Arrival only')
        sheet.write(i, 2, dom_arrival_only, bold)
