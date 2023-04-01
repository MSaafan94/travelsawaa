from odoo import models
class PartnerXlsx(models.AbstractModel):
    _name = 'report.details.quotation_xls'
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
        sheet.write(0, 19, 'flight status int', header)
        sheet.write(0, 20, 'flight type int', header)
        sheet.write(0, 21, 'extra luggage int', header)
        sheet.write(0, 22, 'flight status dom', header)
        sheet.write(0, 23, 'flight type dom', header)
        sheet.write(0, 24, 'extra luggage dom', header)
        sheet.write(0, 25, 'visa type', header)
        sheet.write(0, 26, 'visa situation', header)
        sheet.write(0, 27, 'Embassy Appointment Date', header)
        sheet.write(0, 28, 'Receiving date', header)
        sheet.write(0, 29, 'passport number', header)
        sheet.write(0, 30, 'Birthday', header)
        sheet.write(0, 31, 'passport expire date', header)
        sheet.write(0, 32, 'program status', header)
        sheet.write(0, 33, 'program name', header)
        sheet.write(0, 34, 'Medical Insurance', header)
        sheet.write(0, 35, 'Qr code', header)
        sheet.write(0, 36, 'PCR', header)
        sheet.write(0, 37, 'vaccine type', header)
        sheet.write(0, 38, 'Lase Dose Date', header)
        sheet.write(0, 39, 'Salesperson', header)
        sheet.write(0, 40, 'Total', header)
        sheet.write(0, 41, 'Total paid', header)
        sheet.write(0, 42, 'Total Due', header)
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

        medical_insurance_yes=0
        medical_insurance_no=0

        child_take_program=0
        child_not_take_program=0
        adult_take_program=0
        adult_not_take_program=0


        for obj in quotations:
            # One sheet by partner


            accomodation=list(obj.sale_order_accommodation)
            flight_int=list(obj.sale_order_flight_int)
            flight_dom=list(obj.sale_order_flight_dom)
            visa=list(obj.sale_order_visa_inv)
            name_of_persons=list(obj.name_of_persons)
            name_of_persons.append(obj.partner_id)
            program=list(obj.sale_order_program)
            vaccine=list(obj.sale_order_vaccination_inv)
            medical_insurance=list(obj.sale_order_medical)


            if len(accomodation)==1:
                sheet.write(i, 0,  counter, bold)
                counter += 1
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
                sheet.write(i, 19, flight_int[iterator].flight_status if flight_int[iterator].flight_status else '')
                sheet.write(i, 20, flight_int[iterator].flight_type if flight_int[iterator].flight_type else '')
                sheet.write(i, 21, flight_int[iterator].extra_luggage if flight_int[iterator].extra_luggage else '')
                sheet.write(i, 22, flight_dom[iterator].flight_status if flight_dom[iterator].flight_status else '')
                sheet.write(i, 23, flight_dom[iterator].flight_type if flight_dom[iterator].flight_type else '')
                sheet.write(i, 24, flight_dom[iterator].extra_luggage if flight_dom[iterator].extra_luggage else '')
                sheet.write(i, 25, visa[iterator].visa_type if visa[iterator].visa_type else '')
                sheet.write(i, 26, visa[iterator].visa_situation if visa[iterator].visa_situation else '')
                sheet.write(i, 27, f'{visa[iterator].embassy_appointment}' if visa[iterator].embassy_appointment else '')
                sheet.write(i, 28, visa[iterator].receiving_date if visa[iterator].receiving_date else '')
                sheet.write(i, 29, name_of_persons[iterator].passport_num if name_of_persons[iterator].passport_num else '')
                sheet.write(i, 30,f'{accomodation[iterator].date_of_birth}' if accomodation[iterator].date_of_birth else '')
                sheet.write(i, 31, f'{name_of_persons[iterator].passport_expiry}' if name_of_persons[iterator].passport_expiry else '')
                sheet.write(i, 32, program[iterator].status if program[iterator].status else '')
                names=''
                for name in program[iterator].program_name:
                    print(name)
                    names+= name.name+' ,' if name else ''
                sheet.write(i, 33, names)
                sheet.write(i, 34, medical_insurance[iterator].medical_insurance if medical_insurance[iterator].medical_insurance else '')
                sheet.write(i, 35, vaccine[iterator].qr_code if vaccine[iterator].qr_code else '')
                sheet.write(i, 36, vaccine[iterator].pcr_required.name if vaccine[iterator].pcr_required.name else '')
                sheet.write(i, 37, dict(self.env['sale.order.vaccination']._fields['vaccine_type'].selection).get(vaccine[iterator].vaccine_type) if vaccine[iterator].vaccine_type else '')
                sheet.write(i, 38, f'{vaccine[iterator].last_dose_date}' if vaccine[iterator].last_dose_date else '')
                sheet.write(i, 39, obj.user_id.name if obj.user_id else '')
                sheet.write(i, 40, obj.amount_total if obj.amount_total else '')
                sheet.write(i, 41, obj.total_payments if obj.total_payments else '')
                sheet.write(i, 42, obj.total_due if obj.total_due else '')
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

            child_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'child' and item.program_name))
            adult_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'adult' and item.program_name))
            child_not_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'child' and not item.program_name))
            adult_not_take_program += len(obj.sale_order_program.filtered(lambda item: item.age_type == 'adult' and not item.program_name))
            medical_insurance_yes += len(obj.sale_order_medical.filtered(lambda item: item.medical_insurance == '1'))
            medical_insurance_no += len(obj.sale_order_medical.filtered(lambda item: item.medical_insurance == '2'))
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
        i += 2

        sheet.write(i, 1, 'medical insurance', header)
        sheet.write(i, 2, 'total', header)
        i += 1
        sheet.merge_range(i, 0, i + 1, 0, 'medical insurance', leftheader)
        sheet.write(i, 1, 'yes')
        sheet.write(i, 2, medical_insurance_yes, bold)
        i+=1
        sheet.write(i, 1, 'no')
        sheet.write(i, 2, medical_insurance_no, bold)

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






