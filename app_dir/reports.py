# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import portrait, A4
from connect import create_connection, close_connection
from reportlab.rl_config import defaultPageSize
from func import cinema_stats, list_of_cinemas
import xlsxwriter


def generate_pdf():
    '''his methods generates pdf report of cinemas statistics
    There are informations like: total sum of selled tickets or total income'''
    pdf_filename = 'cinemas_report.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=portrait(A4))

    w = defaultPageSize[0]
    h = defaultPageSize[1]

    c.setFont('Helvetica', 35, leading=None)
    c.drawCentredString(w / 2, 740, "Reports of the Cinemas")

    cinemas = list_of_cinemas()
    cinemas_stats = cinema_stats()
    cnx, cursor = create_connection()
    for name, cinema_id in cinemas:
        c.setFontSize(20)
        c.drawCentredString(w / 2, 600, name)
        c.setFontSize(16)
        text = "Total sum of selled tickets: {}".format(
            cinemas_stats[cinema_id][0])
        c.drawString(w / 10, 520, text)
        text = "Averrage amount of tickets selled per movie: {}".format(
            cinemas_stats[cinema_id][1])
        c.drawString(w / 10, 490, text)
        text = "Percentage: {}".format(
            cinemas_stats[cinema_id][2])
        c.drawString(w / 10, 460, text)
        text = "Total income: {} PLN".format(
            cinemas_stats[cinema_id][3])
        c.drawString(w / 10, 430, text)
        c.showPage()
    close_connection(cnx, cursor)
    c.save()
    return True


def generate_xls():
    '''This methods generates xls document of cinemas statistics
    There are informations like: total sum of selled tickets or total income'''
    xls_filename = 'raport.xls'
    cnx, cursor = create_connection()
    workbook = xlsxwriter.Workbook(xls_filename)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    bold.set_align('center')

    # Add a number format for cells with money.
    money_format = workbook.add_format({'num_format': '#,##0 ZŁ'})
    money_format.set_align('center')

    # Adjust the column width.
    worksheet.set_column(1, 0, 40)
    worksheet.set_column(1, 1, 40)
    worksheet.set_column(1, 2, 40)
    worksheet.set_column(1, 3, 40)

    # center cells
    cell_format = workbook.add_format()
    cell_format.set_align('center')

    worksheet.write('A1', "Cinemas", bold)
    worksheet.write('A2', 'Selled tickets', bold)
    worksheet.write('A3', 'Tickets per movie', bold)
    worksheet.write('A4', 'Total Income', bold)

    info = cinema_stats()
    row = 0
    col = 1
    for cinema_id in info:
        sql = '''
        SELECT name FROM cinemas 
        WHERE cinema_id = %s
        '''
        cursor.execute(sql, (cinema_id,))
        cinema_name = cursor.fetchone()[0]
        worksheet.write(row, col, cinema_name, bold)
        worksheet.write(row + 1, col, info[cinema_id][0], cell_format)
        worksheet.write(row + 2, col, info[cinema_id][1], cell_format)
        worksheet.write(row + 3, col, info[cinema_id][3], cell_format)
        col += 1
    close_connection(cnx, cursor)
