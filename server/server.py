#!/usr/bin/python
import mysql.connector
# import urlparse
import xmlrpclib
import json
# import datetime
from furl import furl
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from urlparse import parse_qsl, urlparse


PORT_NUMBER = 8080

#This class will handles any incoming request from the browser 
class HTTPHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
    url = ''
    db = ''
    username = ''
    password = ''
    uid = 0
    models = 0
    userType = "staff"
        
    def login(self, user, psw):
        global url, db, username, password, uid, models
        url = 'http://10.43.61.20:8069'
        db = 'odoo'
        username =  user
        password = psw

        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        output = common.version()
        print output

        uid = common.authenticate(db, username, password, {})
        print uid

        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

    def getProducts(self, item):
        global db, uid, password
        items = models.execute_kw(db, uid, password,
            'product.product', 'search_read',
            [[['categ_id', '=', 'Ticketeable'], ['code', '=', item]]], {'fields': ['name', 'code']})
        return items

    def getODOOInventory(self, itemID)  :
        if (uid == 1):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.getProducts(itemID)))
        else: 
            self.send_response(403)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write("Unauthenticated")
            
    def assignTicket(self, area, ticket_id):
        print area
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="root",
            database="labweb"
        )

        mycursor = mydb.cursor()
        sql = "SELECT EMPLOYEE_ID, NUM_TICKETS FROM labweb.employees WHERE AREA = %s"
        val = (area, )
        mycursor.execute(sql, val)
        employees = mycursor.fetchall()
        lowest = 9999999
        lowest_id = ""
        for emp in employees:
            if emp[1] < lowest:
                lowest = emp[1]
                lowest_id = emp[0]
        # print lowest_id

        # Assign the ticket
        sql = "INSERT INTO labweb.employee_tickets VALUES (%s, %s)"
        val = (ticket_id ,lowest_id)
        mycursor.execute(sql, val)
        mydb.commit()

        # Update tickets assigned
        sql = "UPDATE labweb.employees SET NUM_TICKETS = %s WHERE EMPLOYEE_ID = %s"
        lowest += 1
        val = (lowest, lowest_id)
        mycursor.execute(sql, val)
        mydb.commit()

    def changeCompanyName(self, mail, rol, area):
        userId = models.execute_kw(db, uid, password,'res.users', 'search_read',[[['login', '=', mail]]], {'fields': ['id']})
        idIndex = userId[0]
        idFinal = idIndex['id']
        models.execute_kw(db, uid, password, 'res.users', 'write', [[idFinal], {
        'company_name': rol,
        }])
        models.execute_kw(db, uid, password, 'res.users', 'write', [[idFinal], {
        'commercial_company_name': area,
        }])
    
    def getUsers(self):
        users = models.execute_kw(db, uid, password,
            'res.users', 'search_read',
            [], {'fields': ['login', 'id']})

    
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(users,  default=str))

    def getUserId(self, login):
        userID = models.execute_kw(db, uid, password,
            'res.users', 'search_read',
            [[["login", '=', login]]], {'fields': ['id']})

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(userID,  default=str))
            
    def do_GET(self)  :
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="root",
            database="labweb"
        )
    
        ### HANDLE DIFFERENT GET PATHS IN URL (ENDPOINTS)
         
        if self.path == '/ongoing':

            mycursor = mydb.cursor()
            sql = "SELECT TKT_ID, DATE FROM labweb.TICKETS WHERE status = 0"
            mycursor.execute(sql)
            res = mycursor.fetchall()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res,  default=str))

        elif self.path == '/pending':

            mycursor = mydb.cursor()
            sql = "SELECT TKT_ID, DATE FROM labweb.TICKETS WHERE status = 1"
            mycursor.execute(sql)
            res = mycursor.fetchall()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res,  default=str))

        elif self.path == '/fixed':

            mycursor = mydb.cursor()
            sql = "SELECT TKT_ID, DATE FROM labweb.TICKETS WHERE status = 2"
            mycursor.execute(sql)
            res = mycursor.fetchall()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res,  default=str))

        elif self.path.startswith('/tickets?'):
            params = furl(self.path)
            tkt_id= params.args['id']
        
            mycursor = mydb.cursor()
            sql = "SELECT * FROM labweb.TICKETS WHERE TKT_ID =  '" + tkt_id + "'"
            # val = (tkt_id)
            mycursor.execute(sql)
            res = mycursor.fetchall()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res, default=str))

        elif self.path.startswith('/inventory?item'):
            params = furl(self.path)
            item_id = params.args['item']
            self.getODOOInventory(item_id)
            
        elif (self.path.startswith('/getTicketsToFix')):
            user = '01226136'
            mycursor = mydb.cursor()
            sql = "SELECT employee_tickets.TKT_ID, tickets.DATE FROM labweb.employee_tickets, labweb.tickets WHERE EMPLOYEE_ID = '" + user + "' AND employee_tickets.TKT_ID = tickets.TKT_ID"
            print sql
            mycursor.execute(sql)
            res = mycursor.fetchall()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res, default= str))
            
        elif self.path == '/admin':
            mycursor = mydb.cursor()
            sql = "SELECT * FROM labweb.TICKETS"
            mycursor.execute(sql)
            res = mycursor.fetchall()
        
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(res,  default=str))

        elif self.path.startswith('/dropdown'):
            #getUserstByID or getUsers
            self.getUsers()

        return
    
    def do_POST(self) :
        print self.path
        if self.path.startswith('/login?'):
            params = furl(self.path)
            user =  params.args['user']
            psw =  params.args['psw']
            self.login(user, psw)
            if uid == 1:
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write("success")

        elif self.path.startswith('/addTicket?'):
            params = furl(self.path)
            item =  params.args['item']
            desc =  params.args['desc']
            loc =  params.args['loc']
            area = params.args['area']
            blob = "424D5E070000000000003E00000028000000EF000000390000000100010000000000200700000000000000000000020000000000000000000000FFFFFF00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000E00003FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000E000007FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000E3FFF80FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000E7FFFFC3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000E7FFFFF8FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000E7FFFFFE7FFFFFFFFFFFFFFFFFFFFFFFF001FFFFFFFFFFFFFFFFFFFFFFFE0000E7FFFFFF7FFFFFFFFFFFFFFFFFF83FFFC0FE7FFFFFFFFFFFFFFFFFFFFFFE0000E7FFFFFFBFFFFFFFFFFFFFFFFFF01FFF07FF9FFFFFFFFFFFFFFFFFFFFFFE0000C7FFFFFFDFFFFFFFFFFFFFFFFFE0EFFE0FFFE3FFFFFFFFFFFC0FFE007FFE0000C7FFFFFFEFFFFFFFFFFFFFFFFFE3EFFC3FFFFBFFFFFFFFFFE0F7F80FBFFE0000C7FFFFFFEFFFFFFC1FFFFFFFFFE3EFFC7FFFFDFFFFFFFFFFC7FBF03FBFFE0000C7FFFFFFEFFFFFF007FFFFFFE0E3EFFC7FFFFDFFFE01FFFF8FFBF0FFBFFE0000C7FFFFFFEFFFFFE0F7FFFFFF80E3EFFC7FFFFEFFFE307FFF1FFBE3FFBFFE0000C7FFFFFFEFFFFFE3FBFFFFFF0763EFFE7FFFFEFC3E7F77FF1FFBC7FFBFFE0000C7FFFFFFEFFFFFE3FDFFFFFE1F63F7FE7F07FF7800FF70FE3FFDC7FFBFFE0000C7FFFFFFEFFFFFF3FDFFFFFC7F63F7FF3EF9FF78E0FF633E3FFD8FFF7FFE0000C7FFFFFFEFFFFFF3FEFFFFFCFF67F7FF9DFCFF71FFFF63BC3FFD9FFCFFFE0000CFFFFFFFEFFFFFF9FEFFC0F8FF47FBFFC3FCFFB1FFFF63CC7FFB1FF3FFFE0000CFE000FFDFFC03F8FF7E0030FF07F9FFFFFC7FB1FFFF67F47FE73FCFFFFE0000CFDFFEFFDFF830FEFFBC1FB1FC8FFEFFFFFE3FB3FFFF47F4FFDE7FBFFFFE0000CF9FFEFFBFF0FE7E7FBC3FB1FB8FFF7FFFFE3FD3FFFF47F4FFBE7F9FFFFE0000CF1FFC7F7FE1FF3F3FDC7FD3F78FFFBFFFFE3FD3FFFF47F0FF3E7F8FFFFE00008F9FE0FF7FE3FFBF3FDC7FD3F7CFFFDFFFFE3FD3FFFF4FF8FF7E7FC7FFFE00008F8000FEFFE3FFDF9FDC7FD3F3E43FEFFFFE3FD3FFFF4FF8FF7CFFE3FFFE00008FC003FC3FC7FFDF9FDC7FB3F87BBFEFFFFE3FD3FFFF4FF8FF7CFFF3FFFE00008FFEFFF007C7FFEF9FDC7F73FF3FCFEFFFFE3FD3F1FF0FF0FFBCFFF9FFFE00008FFFFFC001C7C3EF1FDC7EFBFF9FF7EFFFFE3FF3F6FF0FF4FFBCFFF9FFFE00008FFFFE21FCC7D9EE1FDC7DF9FFEFFBEFFFFE3FE3F6FF0FF4FFDCFCFCFFFE00008FFFFEC3FF07D8E43FBC7DF9E0F7FC0FFFFE3FD3F67F0FF47FE4FB3EFFFE00008FFFFF47FF87D8F07F7C7DFCEE77FFFFFFFE3FD3F73F0FE47FF2FB9EFFFE00008FFFFF47FFC7D8F0FF007C02EE77FFFFFFFE3FD3F73F0FEE7FFC7B1DFFFE00009FFFFF8FFFC7D0F0FE07FE02F477FFFFFFFC3FD3F73F4C4E7FFD7C3DFFFE00009FFFFF8FFFE7D1E1FE8FFFFCF877FFFFFFFC7FD3F73F41BE3FFD7C3BFFFE00009FFFFF8FC3E3E1E1FD8FFFFE78F7FFFFFFFC7FD3F73F6CFE3FFDBFFBFFFE00009FFFFF8F9BE3F1E3FDCFFFFEBFF7FFFFFFFC7FD3FB3F787F3FFDBFFBFFFE00009E07FF8FB9F3FFE3FDCFFFFEDFEFFFFFFFFC7FD9FB3F783F1FFDDFF7FFFE00009EF9FF8F79F1FFE3FDE7FFFEE79FFFFFFFF87FD9FBBF71DF9FFDEFCFFFFE00009EFDFF0F39F5FFE3FEE7FFFDF87FFFFFFFF8FFDDFB9F73DF9FFDF03FFFFE00001EFDFF4FB9E6FFC9FF381F03FFFFFFFFFFF8FF9DFB9FA3EFCFFBFFFFFFFE00001EF0FEEF91EF7FBCFFCF9F7FFFFFFFFFFFF0FFBE03DFA7EFCFFBFFFFFFFE00001E01FEE7D1EFBF7E7FF78FBFFFFFFFFFFFF1FFBFFFCFA7EFC7FBFFFFFFFE00001E01FEE7C1CFDE7F7FFB8FBFFFFFFFFFFFF1FFBFFFE7A7EFE3F7FFFFFFFE00001FFFFEF7E3CFE1FFBFFB8FBFFFFFFFFFFFF1FFBFFFF027EFF1F7FFFFFFFE00001FFFFCF3FFDFFFFFDFFB8FBFFFFFFFFFFFF3FF7FFFFFF7EFFCEFFFFFFFFE00009FFFF9FBFFDFFFFFEFFBCFBFFFFFFFFFFFF3FF7FFFFFF3EFFF0FFFFFFFFE0000C7FFE7FDFFDFFFFFF7F7CFBFFFFFFFFFFFE3FF7FFFFFF3EFFFFFFFFFFFFE0000F03F9FFEFFDFFFFFF7F7C7BFFFFFFFFFFFE7FF7FFFFFFBDFFFFFFFFFFFFE0000FF807FFEFFBFFFFFF9EFE7BFFFFFFFFFFFE7FF7FFFFFFDBFFFFFFFFFFFFE0000FFFDFFFF7F3FFFFFFE1FF07FFFFFFFFFFFC7FF7FFFFFFE3FFFFFFFFFFFFE0000FFFFFFFF40FFFFFFFFFFFFFFFFFFFFFFFFE7FEFFFFFFFFFFFFFFFFFFFFFE0000FFFFFFFFBFFFFFFFFFFFFFFFFFFFFFFFFFF3F1FFFFFFFFFFFFFFFFFFFFFE0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC0FFFFFFFFFFFFFFFFFFFFFFE0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0000"

            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="root",
                database="labweb"
            )
            mycursor = mydb.cursor()
            # ITEM_ID, TKT_ID, DESCRIPTION, LOCATION, STATUS, IMG, AREA
            sql = "INSERT INTO labweb.TICKETS(ITEM_ID, DESCRIPTION, LOCATION, IMG, AREA, SUBMITTED_BY) VALUES (%s, %s, %s, %s, %s, %s)"
            val = ( item, desc , loc, blob, area, username)
            try:
                mycursor.execute(sql, val)
                mydb.commit()
                #  Query to obtain the last added ticket and assign it.
                sql = "SELECT TKT_ID FROM labweb.tickets ORDER BY TKT_ID DESC LIMIT 1"
                mycursor.execute(sql)
                res = mycursor.fetchone()
                ticket_id = res[0]

                self.assignTicket(area, ticket_id)
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                # Send the html message
                self.wfile.write("Ticket added")
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))
                self.send_response(409)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write("Something Happened...")

        elif self.path.startswith('/updateUser'):
            print self.path
            params = furl(self.path)
            mail =  params.args['login']
            rol =  params.args['rol']
            area =  params.args['area']

            self.changeCompanyName(mail, rol, area)



            # changeCompanyName(mail, rol, area) 
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write("Something Happened...")
        
        elif self.path.startswith('/updateTicket?'):

            params = furl(self.path)
            status =  params.args['status']
            tkt_id =  params.args['id']

            mydb = mysql.connector.connect(
                            host="127.0.0.1",
                            user="root",
                            passwd="root",
                            database="labweb"
                        )
            mycursor = mydb.cursor()
            sql = "UPDATE labweb.tickets SET status = %s WHERE TKT_ID = %s";
            val = (status, tkt_id)
            mycursor.execute(sql, val)
            mydb.commit()
            
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # Send the html message
            self.wfile.write("Success")

        return   

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), HTTPHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	